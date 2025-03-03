# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import hashlib
import logging
import os.path
import tempfile
import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import List, Dict, Optional, Union, Callable

from azure.ai.ml._utils._asset_utils import get_object_hash
from azure.ai.ml._utils.utils import is_on_disk_cache_enabled, is_concurrent_component_registration_enabled, \
    is_private_preview_enabled, write_to_shared_file
from azure.ai.ml.constants._common import AzureMLResourceType, AZUREML_COMPONENT_REGISTRATION_MAX_WORKERS
from azure.ai.ml.entities import Component
from azure.ai.ml.entities._builders import BaseNode


logger = logging.getLogger(__name__)

_ANONYMOUS_HASH_PREFIX = "anonymous-component-"
_YAML_SOURCE_PREFIX = "yaml-source-"
_CODE_INVOLVED_PREFIX = "code-involved-"
EXPIRE_TIME_IN_SECONDS = 60 * 60 * 24 * 7  # 7 days

_node_resolution_lock = defaultdict(threading.Lock)


@dataclass
class _CacheContent:
    component_ref: Component
    # in-memory hash assume that the code folders are not changed during the run and
    # use the hash of code path instead of code content to simplify the calculation
    in_memory_hash: str
    # on-disk hash will be calculated base on code content if applicable,
    # so it will work even if the code folders are changed among runs
    on_disk_hash: Optional[str] = None
    arm_id: Optional[str] = None


class CachedNodeResolver(object):
    """Class to resolve component in nodes with cached component resolution results.

    This class is thread-safe if:
    1) self._resolve_nodes is not called concurrently. We guarantee this with a lock in self.resolve_nodes.
        a) self._resolve_nodes won't be called recursively as all nodes will be skipped on
          calling self.register_node_for_lazy_resolution.
        b) it can't be called concurrently as node resolution involves filling back and will change the
          state of nodes, e.g., hash of its inner component.
    2) self._resolve_component is only called concurrently on independent components
        a) we have used an in-memory component hash to deduplicate components to resolve first;
        b) dependent components have been resolved before registered as nodes are registered & resolved
          layer by layer;
        c) dependent code will never be an instance, so it won't cause cache hit issue described in d;
        d) resolution of potential shared dependencies (1 instance used in 2 components) other than components
          are thread-safe as they do not involve further dependency resolution. However, it's still a good practice to
          resolve them before calling self.register_node_for_lazy_resolution as it will impact cache hit rate.
          For example, if:
          node1.component, node2.component = Component(environment=env1, ...), Component(environment=env1, ...)
          root
           |        \
          subgraph  node2
            |
          node1
          when registering node1, its component will be:
          {
              "name": "component1",
              "environment": {
                  ...
              }
              ...
          }
          Its in-memory hash will be `hash_a` on registration.
          Then when registering node2, the component will be:
          {
              "name": "component1",
              "environment": "/subscriptions/.../environments/...",
              ...
          }
          Its in-memory hash will be `hash_b`, which will be a cache miss.
    """

    def __init__(
        self,
        resolver: Callable[[Union[Component, str]], str],
        subscription_id: Optional[str],
        resource_group_name: Optional[str],
        workspace_name: Optional[str],
        registry_name: Optional[str],
    ):
        self._resolver = resolver
        self._cache: Dict[str, _CacheContent] = {}
        self._nodes_to_resolve: List[BaseNode] = []

        self._client_hash = self._get_client_hash(
            subscription_id, resource_group_name, workspace_name, registry_name
        )
        # the same client share 1 lock
        self._lock = _node_resolution_lock[self._client_hash]

    @staticmethod
    def _get_client_hash(
        subscription_id: Optional[str],
        resource_group_name: Optional[str],
        workspace_name: Optional[str],
        registry_name: Optional[str],
    ) -> str:
        """Get a hash for used client.
        Works for both workspace client and registry client.
        """
        object_hash = hashlib.sha256()
        for s in [subscription_id, resource_group_name, workspace_name, registry_name]:
            object_hash.update(str(s).encode("utf-8"))
        return object_hash.hexdigest()

    @staticmethod
    def _get_component_registration_max_workers():
        """Get the max workers for component registration.

        Before Python 3.8, the default max_worker is the number of processors multiplied by 5.
        It may send a large number of the uploading snapshot requests that will occur remote refuses requests.
        In order to avoid retrying the upload requests, max_worker will use the default value in Python 3.8,
        min(32, os.cpu_count + 4).

        1 risk is that, asset_utils will create a new thread pool to upload files in subprocesses, which may cause
        the number of threads exceed the max_worker.
        """
        default_max_workers = min(32, (os.cpu_count() or 1) + 4)
        try:
            max_workers = int(os.environ.get(AZUREML_COMPONENT_REGISTRATION_MAX_WORKERS, default_max_workers))
        except ValueError:
            logger.info(
                "Environment variable %s with value %s set but failed to parse. "
                "Use the default max_worker %s as registration thread pool max_worker."
                "Please reset the value to an integer.",
                AZUREML_COMPONENT_REGISTRATION_MAX_WORKERS,
                os.environ.get(AZUREML_COMPONENT_REGISTRATION_MAX_WORKERS),
                default_max_workers
            )
            max_workers = default_max_workers
        return max_workers

    @staticmethod
    def _get_in_memory_hash_for_component(component: Component) -> str:
        """Get a hash for a component.
        This function assumes that there is no change in code folder among hash calculations,
        which is true during resolution of 1 root pipeline component/job.
        """
        if not isinstance(component, Component):
            # this shouldn't happen; handle it in case invalid call is made outside this class
            raise ValueError(f"Component {component} is not a Component object.")

        # For components with code, its code will be an absolute path before uploaded to blob,
        # so we can use a mixture of its anonymous hash and its source path as its hash, in case
        # there are 2 components with same code but different ignore files
        # Here we can check if the component has a source path instead of check if it has code, as
        # there is no harm to add a source path to the hash even if the component doesn't have code
        # Note that here we assume that the content of code folder won't change during the submission
        if component._source_path:  # pylint: disable=protected-access
            object_hash = hashlib.sha256()
            object_hash.update(component._get_anonymous_hash().encode("utf-8"))  # pylint: disable=protected-access
            object_hash.update(component._source_path.encode("utf-8"))  # pylint: disable=protected-access
            return _YAML_SOURCE_PREFIX + object_hash.hexdigest()
        # For components without code, like pipeline component, their dependencies have already
        # been resolved before calling this function, so we can use their anonymous hash directly
        return _ANONYMOUS_HASH_PREFIX + component._get_anonymous_hash()  # pylint: disable=protected-access

    @staticmethod
    def _get_on_disk_hash_for_component(component: Component, in_memory_hash: str) -> str:
        """Get a hash for a component.
        This function will calculate the hash based on the component's code folder if the component has code,
        so it's unique even if code folder is changed.
        """
        if not isinstance(component, Component):
            # this shouldn't happen; handle it in case invalid call is made outside this class
            raise ValueError(f"Component {component} is not a Component object.")

        # TODO: calculate hash without resolving additional includes (copy code to temp folder)
        # note that it's still thread-safe with current implementation, as only read operations are
        # done on the original code folder
        with component._resolve_local_code() as code:  # pylint: disable=protected-access
            if code is None or code._is_remote:  # pylint: disable=protected-access
                return in_memory_hash

            if hasattr(code, "_upload_hash"):
                content_hash = code._upload_hash  # pylint: disable=protected-access
            else:
                path = code.path if os.path.isabs(code.path) else os.path.join(code.base_path, code.path)
                if os.path.exists(path):
                    content_hash = get_object_hash(path)
                else:
                    # this will be gated by schema validation, so it shouldn't happen except for mock tests
                    return in_memory_hash

            object_hash = hashlib.sha256()
            object_hash.update(in_memory_hash.encode("utf-8"))

            object_hash.update(content_hash.encode("utf-8"))
            return _CODE_INVOLVED_PREFIX + object_hash.hexdigest()

    @property
    def _on_disk_cache_dir(self) -> Path:
        """Get the base path for on disk cache."""
        from azure.ai.ml._version import VERSION
        return Path(tempfile.gettempdir()).joinpath(
            ".azureml",
            "azure-ai-ml",
            VERSION,
            "cache",
            self._client_hash,
            "components",
        )

    def _get_on_disk_cache_path(self, on_disk_hash: str) -> Path:
        """Get the on disk cache path for a component."""
        return self._on_disk_cache_dir.joinpath(on_disk_hash)

    def _load_from_on_disk_cache(self, on_disk_hash: str) -> Optional[str]:
        """Load component arm id from on disk cache."""
        # on-disk cache will expire in a new SDK version
        on_disk_cache_path = self._get_on_disk_cache_path(on_disk_hash)
        if on_disk_cache_path.is_file() and time.time() - on_disk_cache_path.stat().st_ctime < EXPIRE_TIME_IN_SECONDS:
            try:
                return on_disk_cache_path.read_text().strip()
            except (OSError, PermissionError) as e:
                logger.warning(
                    "Failed to read on-disk cache for component due to %s. "
                    "Please check if the file %s is in use or current user doesn't have the permission.",
                    type(e).__name__,
                    on_disk_cache_path.as_posix(),
                )
        return None

    def _save_to_on_disk_cache(self, on_disk_hash: str, arm_id: str) -> None:
        """Save component arm id to on disk cache."""
        # this shouldn't happen in real case, but in case of current mock tests and potential future changes
        if not isinstance(arm_id, str):
            return
        on_disk_cache_path = self._get_on_disk_cache_path(on_disk_hash)
        on_disk_cache_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            write_to_shared_file(on_disk_cache_path, arm_id)
        except PermissionError:
            logger.warning(
                "Failed to save on-disk cache for component due to permission error. "
                "Please check if the file %s is in use or current user doesn't have the permission.",
                on_disk_cache_path.as_posix(),
            )

    def _resolve_cache_contents(self, cache_contents_to_resolve: List[_CacheContent], resolver):
        """Resolve all components to resolve and save the results in cache.
        """
        _components = list(map(lambda x: x.component_ref, cache_contents_to_resolve))
        _map_func = partial(resolver, azureml_type=AzureMLResourceType.COMPONENT)

        if len(_components) > 1 and is_concurrent_component_registration_enabled() and is_private_preview_enabled():
            # given deduplication has already been done, we can safely assume that there is no
            # conflict in concurrent local cache access
            with ThreadPoolExecutor(max_workers=self._get_component_registration_max_workers()) as executor:
                resolution_results = executor.map(_map_func, _components)
        else:
            resolution_results = map(_map_func, _components)

        for cache_content, resolution_results in zip(cache_contents_to_resolve, resolution_results):
            cache_content.arm_id = resolution_results
            if is_on_disk_cache_enabled() and is_private_preview_enabled():
                self._save_to_on_disk_cache(cache_content.on_disk_hash, cache_content.arm_id)

    def _prepare_items_to_resolve(self):
        """Pop all nodes in self._nodes_to_resolve to prepare cache contents to resolve and nodes to resolve.
        Nodes in self._nodes_to_resolve will be grouped by component hash and saved to a dict of list.
        Distinct dependent components not in current cache will be saved to a list.

        :return: a tuple of (dict of nodes to resolve, list of cache contents to resolve)
        """
        _components = list(map(lambda x: x._component, self._nodes_to_resolve))  # pylint: disable=protected-access
        # we can do concurrent component in-memory hash calculation here
        in_memory_component_hashes = map(self._get_in_memory_hash_for_component, _components)

        dict_of_nodes_to_resolve = defaultdict(list)
        cache_contents_to_resolve: List[_CacheContent] = []
        for node, component_hash in zip(self._nodes_to_resolve, in_memory_component_hashes):
            dict_of_nodes_to_resolve[component_hash].append(node)
            if component_hash not in self._cache:
                cache_content = _CacheContent(
                    component_ref=node._component,  # pylint: disable=protected-access
                    in_memory_hash=component_hash,
                )
                self._cache[component_hash] = cache_content
                cache_contents_to_resolve.append(cache_content)
        self._nodes_to_resolve.clear()
        return dict_of_nodes_to_resolve, cache_contents_to_resolve

    def _resolve_cache_contents_from_disk(
        self,
        cache_contents_to_resolve: List[_CacheContent]
    ) -> List[_CacheContent]:
        """Check on-disk cache to resolve cache contents in cache_contents_to_resolve and return
        unresolved cache contents.
        """
        # Note that we should recalculate the hash based on code for local cache, as
        # we can't assume that the code folder won't change among dependency resolution
        for cache_content in cache_contents_to_resolve:
            cache_content.on_disk_hash = self._get_on_disk_hash_for_component(
                cache_content.component_ref,
                cache_content.in_memory_hash
            )

        left_cache_contents_to_resolve = []
        # need to deduplicate disk hash first if concurrent resolution is enabled
        for cache_content in cache_contents_to_resolve:
            cache_content.arm_id = self._load_from_on_disk_cache(cache_content.on_disk_hash)
            if not cache_content.arm_id:
                left_cache_contents_to_resolve.append(cache_content)

        return left_cache_contents_to_resolve

    def _fill_back_component_to_nodes(self, dict_of_nodes_to_resolve: Dict[str, List[BaseNode]]):
        """Fill back resolved component to nodes."""
        for component_hash, nodes in dict_of_nodes_to_resolve.items():
            cache_content = self._cache[component_hash]
            for node in nodes:
                node._component = cache_content.arm_id  # pylint: disable=protected-access

    def _resolve_nodes(self):
        """Processing logic of self.resolve_nodes.
        Should not be called in subgraph creation.
        """
        dict_of_nodes_to_resolve, cache_contents_to_resolve = self._prepare_items_to_resolve()

        if is_on_disk_cache_enabled() and is_private_preview_enabled():
            cache_contents_to_resolve = self._resolve_cache_contents_from_disk(cache_contents_to_resolve)

        self._resolve_cache_contents(cache_contents_to_resolve, resolver=self._resolver)

        self._fill_back_component_to_nodes(dict_of_nodes_to_resolve)

    def register_node_for_lazy_resolution(self, node: BaseNode):
        """Register a node with its component to resolve.
        """
        component = node._component  # pylint: disable=protected-access

        # directly resolve node and skip registration if the resolution involves no remote call
        # so that all node will be skipped when resolving a subgraph recursively
        if isinstance(component, str):
            node._component = self._resolver(  # pylint: disable=protected-access
                component,
                azureml_type=AzureMLResourceType.COMPONENT
            )
            return
        if component.id is not None:
            node._component = component.id  # pylint: disable=protected-access
            return

        self._nodes_to_resolve.append(node)

    def resolve_nodes(self):
        """Resolve all dependent components with resolver and set resolved component arm id back to newly
        registered nodes. Registered nodes will be cleared after resolution.
        """
        if not self._nodes_to_resolve:
            return

        # Lock here as node resolution involves filling back and will change the
        # state of nodes, e.g. hash of its inner component.
        # This will happen only on concurrent external calls; In 1 external call, all nodes in
        # subgraph will be skipped on register_node_for_lazy_resolution when resolving subgraph
        self._lock.acquire()
        try:
            self._resolve_nodes()
        finally:
            # release lock even if exception happens
            self._lock.release()
