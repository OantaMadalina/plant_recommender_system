from botocore.config import Config
import boto3

s3_client = boto3.client('s3', config=Config(signature_version='s3v4'))


def generate_signed_url(bucket_name, object_key, expiration=3600):
    return s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': object_key},
        ExpiresIn=expiration
    )
