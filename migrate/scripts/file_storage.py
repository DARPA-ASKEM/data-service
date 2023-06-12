#!/usr/bin/env python
import json
import os
import sys
from pathlib import Path

import boto3

STORAGE_HOST = os.getenv("STORAGE_HOST")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_DATASET_PATH = os.getenv("S3_DATASET_PATH")
S3_RESULT_PATH = os.getenv("S3_RESULT_PATH")

migrate_dir = Path(os.path.dirname(__file__))
file_dir = f"{migrate_dir.parent}/seeds/files"
file_dict = json.load(open(f"{migrate_dir.parent}/seeds/files.json", "r"))

s3_paths = {
    "datasets": S3_DATASET_PATH,
    "simulations": S3_RESULT_PATH,
}


def create_bucket(s3_client):
    bucket_response = s3_client.list_buckets()
    buckets = [x["Name"] for x in bucket_response["Buckets"]]

    if S3_BUCKET in buckets:
        print(f"Bucket {S3_BUCKET} exists")
    else:
        print(f"Creating bucket: {S3_BUCKET}")
        s3_client.create_bucket(Bucket=S3_BUCKET)


def upload_file(s3_client, s3_path: str, filename: str):
    file_path = file_dict[filename]
    s3_path_key = s3_paths[s3_path]
    key = f"{s3_path_key}/{file_path}"
    s3_client.upload_file(
        Bucket=S3_BUCKET,
        Filename=f"{file_dir}/{filename}",
        Key=key,
    )


if __name__ == "__main__":
    if STORAGE_HOST:
        s3 = boto3.client(
            "s3",
            endpoint_url=STORAGE_HOST,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=None,
            config=boto3.session.Config(signature_version="s3v4"),
            verify=False,
        )
    else:
        s3 = boto3.client("s3")

    if len(sys.argv) > 1:
        op = sys.argv[1]
        if op == "create_bucket":
            create_bucket(s3)
        elif op == "upload_file":
            s3_path_arg = sys.argv[2]
            for file in os.listdir(file_dir):
                upload_file(s3_client=s3, s3_path=s3_path_arg, filename=file)
