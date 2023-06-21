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
        s3_opts["aws_session_token"] = None
        s3_opts["verify"] = False
        s3_opts["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
        s3_opts["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY
    else:
        s3_opts["region_name"] = settings.AWS_REGION

    s3_ = boto3.client("s3", **s3_opts)

    return s3_


def get_file_path(
    entity_id: str | int, file_name: str, path: str = settings.S3_RESULTS_PATH
) -> str:
    """
    Function builds a file path for s3.
    """
    return os.path.join(path, str(entity_id), file_name)


def get_presigned_url(
    entity_id: str | int,
    file_name: str,
    method: str,
    path: str = settings.S3_RESULTS_PATH,
):
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
