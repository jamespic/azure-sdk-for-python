# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from ._models_py3 import AbsoluteDeleteOption
from ._models_py3 import AdHocBackupRuleOptions
from ._models_py3 import AdhocBackupTriggerOption
from ._models_py3 import AdhocBasedTaggingCriteria
from ._models_py3 import AdhocBasedTriggerContext
from ._models_py3 import AuthCredentials
from ._models_py3 import AzureBackupDiscreteRecoveryPoint
from ._models_py3 import AzureBackupFindRestorableTimeRangesRequest
from ._models_py3 import AzureBackupFindRestorableTimeRangesRequestResource
from ._models_py3 import AzureBackupFindRestorableTimeRangesResponse
from ._models_py3 import AzureBackupFindRestorableTimeRangesResponseResource
from ._models_py3 import AzureBackupJob
from ._models_py3 import AzureBackupJobResource
from ._models_py3 import AzureBackupJobResourceList
from ._models_py3 import AzureBackupParams
from ._models_py3 import AzureBackupRecoveryPoint
from ._models_py3 import AzureBackupRecoveryPointBasedRestoreRequest
from ._models_py3 import AzureBackupRecoveryPointResource
from ._models_py3 import AzureBackupRecoveryPointResourceList
from ._models_py3 import AzureBackupRecoveryTimeBasedRestoreRequest
from ._models_py3 import AzureBackupRehydrationRequest
from ._models_py3 import AzureBackupRestoreRequest
from ._models_py3 import AzureBackupRestoreWithRehydrationRequest
from ._models_py3 import AzureBackupRule
from ._models_py3 import AzureMonitorAlertSettings
from ._models_py3 import AzureOperationalStoreParameters
from ._models_py3 import AzureRetentionRule
from ._models_py3 import BackupCriteria
from ._models_py3 import BackupDatasourceParameters
from ._models_py3 import BackupInstance
from ._models_py3 import BackupInstanceResource
from ._models_py3 import BackupInstanceResourceList
from ._models_py3 import BackupParameters
from ._models_py3 import BackupPolicy
from ._models_py3 import BackupSchedule
from ._models_py3 import BackupVault
from ._models_py3 import BackupVaultResource
from ._models_py3 import BackupVaultResourceList
from ._models_py3 import BaseBackupPolicy
from ._models_py3 import BaseBackupPolicyResource
from ._models_py3 import BaseBackupPolicyResourceList
from ._models_py3 import BasePolicyRule
from ._models_py3 import BlobBackupDatasourceParameters
from ._models_py3 import CheckNameAvailabilityRequest
from ._models_py3 import CheckNameAvailabilityResult
from ._models_py3 import ClientDiscoveryDisplay
from ._models_py3 import ClientDiscoveryForLogSpecification
from ._models_py3 import ClientDiscoveryForProperties
from ._models_py3 import ClientDiscoveryForServiceSpecification
from ._models_py3 import ClientDiscoveryResponse
from ._models_py3 import ClientDiscoveryValueForSingleApi
from ._models_py3 import CopyOnExpiryOption
from ._models_py3 import CopyOption
from ._models_py3 import CustomCopyOption
from ._models_py3 import DataStoreInfoBase
from ._models_py3 import DataStoreParameters
from ._models_py3 import Datasource
from ._models_py3 import DatasourceSet
from ._models_py3 import Day
from ._models_py3 import DeleteOption
from ._models_py3 import DeletedBackupInstance
from ._models_py3 import DeletedBackupInstanceResource
from ._models_py3 import DeletedBackupInstanceResourceList
from ._models_py3 import DeletionInfo
from ._models_py3 import DppBaseResource
from ._models_py3 import DppBaseResourceList
from ._models_py3 import DppIdentityDetails
from ._models_py3 import DppProxyResource
from ._models_py3 import DppResource
from ._models_py3 import DppResourceList
from ._models_py3 import DppTrackedResource
from ._models_py3 import DppTrackedResourceList
from ._models_py3 import DppWorkerRequest
from ._models_py3 import Error
from ._models_py3 import ErrorAdditionalInfo
from ._models_py3 import ExportJobsResult
from ._models_py3 import FeatureValidationRequest
from ._models_py3 import FeatureValidationRequestBase
from ._models_py3 import FeatureValidationResponse
from ._models_py3 import FeatureValidationResponseBase
from ._models_py3 import ImmediateCopyOption
from ._models_py3 import ImmutabilitySettings
from ._models_py3 import InnerError
from ._models_py3 import ItemLevelRestoreCriteria
from ._models_py3 import ItemLevelRestoreTargetInfo
from ._models_py3 import ItemPathBasedRestoreCriteria
from ._models_py3 import JobExtendedInfo
from ._models_py3 import JobSubTask
from ._models_py3 import KubernetesClusterBackupDatasourceParameters
from ._models_py3 import KubernetesClusterRestoreCriteria
from ._models_py3 import KubernetesPVRestoreCriteria
from ._models_py3 import KubernetesStorageClassRestoreCriteria
from ._models_py3 import MonitoringSettings
from ._models_py3 import OperationExtendedInfo
from ._models_py3 import OperationJobExtendedInfo
from ._models_py3 import OperationResource
from ._models_py3 import PatchBackupVaultInput
from ._models_py3 import PatchResourceRequestInput
from ._models_py3 import PolicyInfo
from ._models_py3 import PolicyParameters
from ._models_py3 import ProtectionStatusDetails
from ._models_py3 import RangeBasedItemLevelRestoreCriteria
from ._models_py3 import RecoveryPointDataStoreDetails
from ._models_py3 import RecoveryPointsFilters
from ._models_py3 import ResourceGuard
from ._models_py3 import ResourceGuardOperation
from ._models_py3 import ResourceGuardOperationDetail
from ._models_py3 import ResourceGuardProxyBase
from ._models_py3 import ResourceGuardProxyBaseResource
from ._models_py3 import ResourceGuardProxyBaseResourceList
from ._models_py3 import ResourceGuardResource
from ._models_py3 import ResourceGuardResourceList
from ._models_py3 import ResourceMoveDetails
from ._models_py3 import RestorableTimeRange
from ._models_py3 import RestoreFilesTargetInfo
from ._models_py3 import RestoreJobRecoveryPointDetails
from ._models_py3 import RestoreTargetInfo
from ._models_py3 import RestoreTargetInfoBase
from ._models_py3 import RetentionTag
from ._models_py3 import ScheduleBasedBackupCriteria
from ._models_py3 import ScheduleBasedTriggerContext
from ._models_py3 import SecretStoreBasedAuthCredentials
from ._models_py3 import SecretStoreResource
from ._models_py3 import SecuritySettings
from ._models_py3 import SoftDeleteSettings
from ._models_py3 import SourceLifeCycle
from ._models_py3 import StorageSetting
from ._models_py3 import SupportedFeature
from ._models_py3 import SyncBackupInstanceRequest
from ._models_py3 import SystemData
from ._models_py3 import TaggingCriteria
from ._models_py3 import TargetCopySetting
from ._models_py3 import TargetDetails
from ._models_py3 import TriggerBackupRequest
from ._models_py3 import TriggerContext
from ._models_py3 import UnlockDeleteRequest
from ._models_py3 import UnlockDeleteResponse
from ._models_py3 import UserFacingError
from ._models_py3 import ValidateForBackupRequest
from ._models_py3 import ValidateRestoreRequestObject

from ._data_protection_client_enums import AbsoluteMarker
from ._data_protection_client_enums import AlertsState
from ._data_protection_client_enums import CreatedByType
from ._data_protection_client_enums import CurrentProtectionState
from ._data_protection_client_enums import DataStoreTypes
from ._data_protection_client_enums import DayOfWeek
from ._data_protection_client_enums import ExistingResourcePolicy
from ._data_protection_client_enums import FeatureSupportStatus
from ._data_protection_client_enums import FeatureType
from ._data_protection_client_enums import ImmutabilityState
from ._data_protection_client_enums import Month
from ._data_protection_client_enums import PersistentVolumeRestoreMode
from ._data_protection_client_enums import ProvisioningState
from ._data_protection_client_enums import RecoveryOption
from ._data_protection_client_enums import RehydrationPriority
from ._data_protection_client_enums import RehydrationStatus
from ._data_protection_client_enums import ResourceGuardProvisioningState
from ._data_protection_client_enums import ResourceMoveState
from ._data_protection_client_enums import RestoreSourceDataStoreType
from ._data_protection_client_enums import RestoreTargetLocationType
from ._data_protection_client_enums import SecretStoreType
from ._data_protection_client_enums import SoftDeleteState
from ._data_protection_client_enums import SourceDataStoreType
from ._data_protection_client_enums import Status
from ._data_protection_client_enums import StorageSettingStoreTypes
from ._data_protection_client_enums import StorageSettingTypes
from ._data_protection_client_enums import SyncType
from ._data_protection_client_enums import ValidationType
from ._data_protection_client_enums import WeekNumber
from ._patch import __all__ as _patch_all
from ._patch import *  # pylint: disable=unused-wildcard-import
from ._patch import patch_sdk as _patch_sdk

__all__ = [
    "AbsoluteDeleteOption",
    "AdHocBackupRuleOptions",
    "AdhocBackupTriggerOption",
    "AdhocBasedTaggingCriteria",
    "AdhocBasedTriggerContext",
    "AuthCredentials",
    "AzureBackupDiscreteRecoveryPoint",
    "AzureBackupFindRestorableTimeRangesRequest",
    "AzureBackupFindRestorableTimeRangesRequestResource",
    "AzureBackupFindRestorableTimeRangesResponse",
    "AzureBackupFindRestorableTimeRangesResponseResource",
    "AzureBackupJob",
    "AzureBackupJobResource",
    "AzureBackupJobResourceList",
    "AzureBackupParams",
    "AzureBackupRecoveryPoint",
    "AzureBackupRecoveryPointBasedRestoreRequest",
    "AzureBackupRecoveryPointResource",
    "AzureBackupRecoveryPointResourceList",
    "AzureBackupRecoveryTimeBasedRestoreRequest",
    "AzureBackupRehydrationRequest",
    "AzureBackupRestoreRequest",
    "AzureBackupRestoreWithRehydrationRequest",
    "AzureBackupRule",
    "AzureMonitorAlertSettings",
    "AzureOperationalStoreParameters",
    "AzureRetentionRule",
    "BackupCriteria",
    "BackupDatasourceParameters",
    "BackupInstance",
    "BackupInstanceResource",
    "BackupInstanceResourceList",
    "BackupParameters",
    "BackupPolicy",
    "BackupSchedule",
    "BackupVault",
    "BackupVaultResource",
    "BackupVaultResourceList",
    "BaseBackupPolicy",
    "BaseBackupPolicyResource",
    "BaseBackupPolicyResourceList",
    "BasePolicyRule",
    "BlobBackupDatasourceParameters",
    "CheckNameAvailabilityRequest",
    "CheckNameAvailabilityResult",
    "ClientDiscoveryDisplay",
    "ClientDiscoveryForLogSpecification",
    "ClientDiscoveryForProperties",
    "ClientDiscoveryForServiceSpecification",
    "ClientDiscoveryResponse",
    "ClientDiscoveryValueForSingleApi",
    "CopyOnExpiryOption",
    "CopyOption",
    "CustomCopyOption",
    "DataStoreInfoBase",
    "DataStoreParameters",
    "Datasource",
    "DatasourceSet",
    "Day",
    "DeleteOption",
    "DeletedBackupInstance",
    "DeletedBackupInstanceResource",
    "DeletedBackupInstanceResourceList",
    "DeletionInfo",
    "DppBaseResource",
    "DppBaseResourceList",
    "DppIdentityDetails",
    "DppProxyResource",
    "DppResource",
    "DppResourceList",
    "DppTrackedResource",
    "DppTrackedResourceList",
    "DppWorkerRequest",
    "Error",
    "ErrorAdditionalInfo",
    "ExportJobsResult",
    "FeatureValidationRequest",
    "FeatureValidationRequestBase",
    "FeatureValidationResponse",
    "FeatureValidationResponseBase",
    "ImmediateCopyOption",
    "ImmutabilitySettings",
    "InnerError",
    "ItemLevelRestoreCriteria",
    "ItemLevelRestoreTargetInfo",
    "ItemPathBasedRestoreCriteria",
    "JobExtendedInfo",
    "JobSubTask",
    "KubernetesClusterBackupDatasourceParameters",
    "KubernetesClusterRestoreCriteria",
    "KubernetesPVRestoreCriteria",
    "KubernetesStorageClassRestoreCriteria",
    "MonitoringSettings",
    "OperationExtendedInfo",
    "OperationJobExtendedInfo",
    "OperationResource",
    "PatchBackupVaultInput",
    "PatchResourceRequestInput",
    "PolicyInfo",
    "PolicyParameters",
    "ProtectionStatusDetails",
    "RangeBasedItemLevelRestoreCriteria",
    "RecoveryPointDataStoreDetails",
    "RecoveryPointsFilters",
    "ResourceGuard",
    "ResourceGuardOperation",
    "ResourceGuardOperationDetail",
    "ResourceGuardProxyBase",
    "ResourceGuardProxyBaseResource",
    "ResourceGuardProxyBaseResourceList",
    "ResourceGuardResource",
    "ResourceGuardResourceList",
    "ResourceMoveDetails",
    "RestorableTimeRange",
    "RestoreFilesTargetInfo",
    "RestoreJobRecoveryPointDetails",
    "RestoreTargetInfo",
    "RestoreTargetInfoBase",
    "RetentionTag",
    "ScheduleBasedBackupCriteria",
    "ScheduleBasedTriggerContext",
    "SecretStoreBasedAuthCredentials",
    "SecretStoreResource",
    "SecuritySettings",
    "SoftDeleteSettings",
    "SourceLifeCycle",
    "StorageSetting",
    "SupportedFeature",
    "SyncBackupInstanceRequest",
    "SystemData",
    "TaggingCriteria",
    "TargetCopySetting",
    "TargetDetails",
    "TriggerBackupRequest",
    "TriggerContext",
    "UnlockDeleteRequest",
    "UnlockDeleteResponse",
    "UserFacingError",
    "ValidateForBackupRequest",
    "ValidateRestoreRequestObject",
    "AbsoluteMarker",
    "AlertsState",
    "CreatedByType",
    "CurrentProtectionState",
    "DataStoreTypes",
    "DayOfWeek",
    "ExistingResourcePolicy",
    "FeatureSupportStatus",
    "FeatureType",
    "ImmutabilityState",
    "Month",
    "PersistentVolumeRestoreMode",
    "ProvisioningState",
    "RecoveryOption",
    "RehydrationPriority",
    "RehydrationStatus",
    "ResourceGuardProvisioningState",
    "ResourceMoveState",
    "RestoreSourceDataStoreType",
    "RestoreTargetLocationType",
    "SecretStoreType",
    "SoftDeleteState",
    "SourceDataStoreType",
    "Status",
    "StorageSettingStoreTypes",
    "StorageSettingTypes",
    "SyncType",
    "ValidationType",
    "WeekNumber",
]
__all__.extend([p for p in _patch_all if p not in __all__])
_patch_sdk()
