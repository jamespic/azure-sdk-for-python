# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_single_label_classify_async.py

DESCRIPTION:
    This sample demonstrates how to classify documents into a single custom category. For example,
    movie plot summaries can be categorized into a single movie genre like "Mystery", "Drama", "Thriller",
    "Comedy", "Action", etc. Classifying documents is also available as an action type through
    the begin_analyze_actions API.

    For information on regional support of custom features and how to train a model to
    classify your documents, see https://aka.ms/azsdk/textanalytics/customfunctionalities

USAGE:
    python sample_single_label_classify_async.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_LANGUAGE_ENDPOINT - the endpoint to your Language resource.
    2) AZURE_LANGUAGE_KEY - your Language subscription key
    3) SINGLE_LABEL_CLASSIFY_PROJECT_NAME - your Language Studio project name
    4) SINGLE_LABEL_CLASSIFY_DEPLOYMENT_NAME - your Language Studio deployment name
"""


import os
import asyncio


async def sample_classify_document_single_label_async() -> None:
    # [START single_label_classify_async]
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics.aio import TextAnalyticsClient

    endpoint = os.environ["AZURE_LANGUAGE_ENDPOINT"]
    key = os.environ["AZURE_LANGUAGE_KEY"]
    project_name = os.environ["SINGLE_LABEL_CLASSIFY_PROJECT_NAME"]
    deployment_name = os.environ["SINGLE_LABEL_CLASSIFY_DEPLOYMENT_NAME"]
    path_to_sample_document = os.path.abspath(
        os.path.join(
            os.path.abspath(__file__),
            "..",
            "..",
            "./text_samples/custom_classify_sample.txt",
        )
    )

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    with open(path_to_sample_document) as fd:
        document = [fd.read()]

    async with text_analytics_client:
        poller = await text_analytics_client.begin_single_label_classify(
            document,
            project_name=project_name,
            deployment_name=deployment_name
        )

        pages = await poller.result()

        document_results = []
        async for page in pages:
            document_results.append(page)

    for doc, classification_result in zip(document, document_results):
        if classification_result.kind == "CustomDocumentClassification":
            classification = classification_result.classifications[0]
            print("The document text '{}' was classified as '{}' with confidence score {}.".format(
                doc, classification.category, classification.confidence_score)
            )
        elif classification_result.is_error is True:
            print("Document text '{}' has an error with code '{}' and message '{}'".format(
                doc, classification_result.error.code, classification_result.error.message
            ))
    # [END single_label_classify_async]


async def main():
    await sample_classify_document_single_label_async()


if __name__ == '__main__':
    asyncio.run(main())
