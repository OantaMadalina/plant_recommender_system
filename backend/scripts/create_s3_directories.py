#!/usr/bin/env python

import boto3
import os

stage = os.environ["STAGE"]
accesskey = os.environ["AWS_ACCESS_KEY_ID"]
secretkey = os.environ["AWS_SECRET_ACCESS_KEY"]


def create_s3_directories(bucket, s3_res, keys) -> str:
    for key in keys:
        s3_res.Bucket(bucket).put_object(Body="", Bucket=bucket, Key=key)


if __name__ == "__main__":
    session = boto3.Session(
        aws_access_key_id=accesskey, aws_secret_access_key=secretkey
    )
    s3_res = boto3.resource("s3")
    bucket = f"bootcampengine-{stage}"

    directories = [
        "CMT/TariffPlan/",
        "CMT/Discount/"
    ]
    create_s3_directories(bucket, s3_res, directories)
