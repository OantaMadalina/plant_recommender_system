import os
import boto3

BOOTCAMP_BUCKET = "test"


def get_test_file_path(filename):
    return os.path.join(os.environ["TEST_FILES_DIR"], filename)


def bucket_file_exists(bucket, file):
    s3 = boto3.resource("s3")
    return any(
        obj.bucket_name == bucket and obj.key == file
        for obj in s3.Bucket(BOOTCAMP_BUCKET).objects.all())
