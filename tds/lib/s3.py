"""
TDS S3 storage.
"""
import os

import boto3

from tds.settings import settings


def s3_client():
    """
    Function sets up an S3 client based on env settings.
    """
    s3_opts = {
        "config": boto3.session.Config(signature_version="s3v4"),
    }
    if settings.STORAGE_HOST:
        s3_opts["endpoint_url"] = settings.STORAGE_HOST
    else:
        # @TODO: Deprecate this and use AWS_DEFAULT_REGION in ENV.
        s3_opts["region_name"] = settings.AWS_REGION

    s3_ = boto3.client("s3", **s3_opts)

    return s3_


def get_file_path(entity_id: str | int, file_name: str, path: str) -> str:
    """
    Function builds a file path for s3.
    """
    return os.path.join(path, str(entity_id), file_name)


def get_presigned_url(entity_id: str | int, file_name: str, method: str, path: str):
    """
    Function generates a presigned URL for the HMI client.
    """
    s3_ = s3_client()
    s3_key = get_file_path(entity_id=entity_id, file_name=file_name, path=path)

    presigned_url = s3_.generate_presigned_url(
        ClientMethod=method,
        Params={"Bucket": settings.S3_BUCKET, "Key": s3_key},
        ExpiresIn=1500,
    )

    return presigned_url


def copy_object(origin_path: str, destination_path: str):
    """
    Function copies an object in s3.
    """
    s3_ = s3_client()
    response = s3_.copy_object(
        CopySource=f"{settings.S3_BUCKET}/{origin_path}",
        Bucket=settings.S3_BUCKET,
        Key=destination_path,
    )

    return response


def parse_filename(path: str):
    """
    Function grabs filename via brute force.
    """
    filename = path
    if path.find("http") or path.find("s3"):
        pieces = path.split("/")
        filename = pieces[-1]

        if filename.find("?"):
            filename = filename.split("?")[0]
    return filename
