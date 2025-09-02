from bootcamp_lib.logger import Logger
import boto3

from typing import List

from bootcamp_lib.dynamodb import DynamodbTable
from bootcamp_lib.dynamodb_model import DynamoDbModel
from botocore.config import Config
from botocore.exceptions import ClientError


dynamodb_res = boto3.resource("dynamodb")

s3_client = boto3.client('s3', config=Config(signature_version='s3v4'))


def create_presigned_get(bucket_name, object_key, expiration=3600) -> str:
    return s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': object_key},
        ExpiresIn=expiration
    )


def create_presigned_post(bucket_name, object_name,
                          fields=None, conditions=None, expiration=3600):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    # Generate a presigned S3 POST URL
    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        Logger().error(f"Presigned POST URL could not be generated: {e}")
        return None

    # The response contains the presigned URL and required fields
    return response


def scan_table(table: DynamodbTable, **kwargs) -> List[DynamoDbModel]:
    return table(dynamodb_res).scan(**kwargs)


def get_item(item_key: dict, table: DynamodbTable, **kwargs):
    return table(dynamodb_res).get_item(key=item_key, **kwargs)


def put_item(item: DynamoDbModel, table: DynamodbTable):
    return table(dynamodb_res).put_item(item)


def update_item(item_key: dict, table: DynamodbTable, **kwargs):
    update_expression = kwargs.get("update_expression", "")
    expression_attribute_values = kwargs.get("expression_attribute_values", "")

    return table(dynamodb_res).update_item(key=item_key,
                                           expression=update_expression,
                                           values=expression_attribute_values)


def remove_item(item_key: dict, table: DynamodbTable, **kwargs):
    condition_expression = kwargs.get("condition_expression", None)
    return table(dynamodb_res).delete_item(key=item_key,
                                           condition_expression=condition_expression)
