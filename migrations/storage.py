"""
Storage utilities for use in migrations
"""
import boto3
import requests

from tds.settings import settings


def create_s3_client():
    """
    Generates a boto3 s3 client instance based on the current settings.
    """
    if settings.STORAGE_HOST:
        s3_client = boto3.client(
            "s3",
            endpoint_url=settings.STORAGE_HOST,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            aws_session_token=None,
            config=boto3.session.Config(signature_version="s3v4"),
            verify=False,
        )
    else:
        s3_client = boto3.client("s3")
    return s3_client


def download_file(url: str, file_path: dict):
    """
    Downloads a file, streaming 8 mb at a time to keep memory usage low.
    Allows downloading very large files without running out of memory at a nominal performance cost.
    """
    file_dl = requests.get(url, allow_redirects=True, stream=True, timeout=120)
    with open(file_path, "wb") as downloaded_file:
        while file_dl.raw.length_remaining > 0:
            downloaded_file.write(file_dl.raw.read(8_388_608))  # Download 8mb at a time


def create_bucket(s3_client):
    """
    Function creates a bucket in S3.
    """
    bucket_response = s3_client.list_buckets()
    buckets = [x["Name"] for x in bucket_response["Buckets"]]

    if settings.S3_BUCKET in buckets:
        print(f"Bucket {settings.S3_BUCKET} exists, no need to create.")
    else:
        print(f"Creating bucket: {settings.S3_BUCKET}")
        s3_client.create_bucket(Bucket=settings.S3_BUCKET)


def upload_file(s3_client, file_path, storage_path):
    """
    Function uploads a file to S3.
    """
    s3_client.upload_file(
        Bucket=settings.S3_BUCKET,
        Filename=file_path,
        Key=storage_path,
    )
