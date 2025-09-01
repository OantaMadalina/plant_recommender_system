import os

import boto3

from bootcamp_lib.logger import Logger


class CavendishS3:

    def __init__(self, bucket: str, s3_res=None):
        self._bucket = bucket
        self._s3_res = s3_res or boto3.resource("s3", verify=False)

    def delete_file(self, bucket_file: str):
        Logger().info("Deleting 's3://%s/%s'", self._bucket, bucket_file)
        self._s3_res.Object(self._bucket, bucket_file).delete()
        Logger().info("'s3://%s/%s' deleted", self._bucket, bucket_file)

    def upload_file(self, local_file: str, bucket_file: str):
        file_size = os.path.getsize(local_file)
        Logger().info("Uploading 's3://%s/%s' (%d) bytes", self._bucket, bucket_file, file_size)
        self._s3_res.Bucket(self._bucket).upload_file(Filename=local_file, Key=bucket_file)
        Logger().info("'s3://%s/%s' uploaded", self._bucket, bucket_file)

    def download_file(self, bucket_file: str, local_file: str):
        Logger().debug("Downloading 's3://%s/%s' to %s", self._bucket, bucket_file, local_file)
        self._s3_res.Bucket(self._bucket).download_file(bucket_file, local_file)
        Logger().info("'s3://%s/%s' downloaded", self._bucket, bucket_file)

    def copy_file(self, from_key: str, to_key: str):
        Logger().info("Copying 's3://%s/%s' to 's3://%s/%s'",
                      self._bucket, from_key, self._bucket, to_key)
        self._s3_res.Object(self._bucket, to_key).copy_from(
            CopySource={"Bucket": self._bucket, "Key": from_key})
        Logger().info("Copied 's3://%s/%s' to 's3://%s/%s'", self._bucket, from_key,
                      self._bucket, to_key)

    def archive_file(self, filename: str, archive_dir: str = "Processed"):
        archive_file = "{0}/{1}/{2}".format(
            os.path.dirname(filename), archive_dir, os.path.basename(filename)
        )
        self.copy_file(filename, archive_file)
        self.delete_file(filename)
