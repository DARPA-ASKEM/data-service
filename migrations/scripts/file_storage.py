#!/usr/bin/env python
"""
TDS File Storage Seed file.
"""
import json
import os
import sys
from pathlib import Path

import boto3
import requests

STORAGE_HOST = os.getenv("STORAGE_HOST")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_DATASET_PATH = os.getenv("S3_DATASET_PATH")
S3_RESULTS_PATH = os.getenv("S3_RESULTS_PATH")

migrate_dir = Path(os.path.dirname(__file__))
file_dir = f"{migrate_dir.parent}/seeds/files"
file_dict = json.load(
    # pylint: disable-next=consider-using-with
    open(f"{migrate_dir.parent}/seeds/files.json", "r", encoding="utf-8")
)

s3_paths = {
    "datasets": S3_DATASET_PATH,
    "simulations": S3_RESULTS_PATH,
}


def create_bucket(s3_client):
    """
    Function creates a bucket in S3.
    """
    bucket_response = s3_client.list_buckets()
    buckets = [x["Name"] for x in bucket_response["Buckets"]]

    if S3_BUCKET in buckets:
        print(f"Bucket {S3_BUCKET} exists")
    else:
        print(f"Creating bucket: {S3_BUCKET}")
        s3_client.create_bucket(Bucket=S3_BUCKET)


def upload_file(s3_client, s3_path: str, filename: str):
    """
    Function uploads a file to S3.
    """
    file_path = file_dict[filename]
    if type(file_path) is dict:
        download_dict = file_path
        file_path = file_path["path"]
        download_file(filename, download_dict)

    s3_path_key = s3_paths[s3_path]
    key = f"{s3_path_key}/{file_path}"
    s3_client.upload_file(
        Bucket=S3_BUCKET,
        Filename=f"{file_dir}/{filename}",
        Key=key,
    )


def download_file(name: str, download_dict: dict):
    url, path = download_dict["url"], download_dict["path"]
    print(f"Downloading {name}")
    file_dl = requests.get(url, allow_redirects=True)
    with open(f"{file_dir}/{name}", "w", encoding="utf-8") as dlf:
        dlf.write(file_dl.text)


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
        FILE_OP = sys.argv[1]
        if FILE_OP == "create_bucket":
            create_bucket(s3)
        elif FILE_OP == "upload_file":
            s3_path_arg = sys.argv[2]
            for file in file_dict:
                upload_file(s3_client=s3, s3_path=s3_path_arg, filename=file)
