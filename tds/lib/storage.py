"""File storage library for functions related to getting and putting files.
"""

import csv
import os
import tempfile
from io import StringIO
from urllib.parse import urlparse

import boto3
import botocore
import pandas

# S3 OBJECT
s3 = boto3.client("s3")


def get_rawfile(path):
    """Gets a file from a filepath

    Args:
        path (str): URI to file

    Raises:
        FileNotFoundError: If the file cannnot be found on S3.
        RuntimeError: If the path URI does not begin with 'file' or 's3'
        there is no handler for it yet.

    Returns:
        file: a file-like object
    """
    location_info = urlparse(path)

    if location_info.scheme.lower() == "file":
        return open(location_info.path, "rb")
    if location_info.scheme.lower() == "s3":
        try:
            file_path = location_info.path.lstrip("/")
            raw_file = tempfile.TemporaryFile()
            s3.download_fileobj(
                Bucket=location_info.netloc, Key=file_path, Fileobj=raw_file
            )
            raw_file.seek(0)
        except botocore.exceptions.ClientError as error:
            raise FileNotFoundError() from error
    else:
        raise RuntimeError("File storage format is unknown")

    return raw_file


def put_rawfile(path, fileobj):
    """Puts/uploads a file at URI specified

    Args:
        path (str): URI to put/upload the file to.
        fileobj (file): The file-like object to upload.

    Raises:
        RuntimeError: If the path URI does not begin with 'file' or 's3'
        there is no handler for it yet.
    """
    location_info = urlparse(path)

    if location_info.scheme.lower() == "file":
        if not os.path.isdir(os.path.dirname(location_info.path)):
            os.makedirs(os.path.dirname(location_info.path), exist_ok=True)
        with open(location_info.path, "wb") as output_file:
            output_file.write(fileobj.read())
    elif location_info.scheme.lower() == "s3":
        output_path = location_info.path.lstrip("/")
        s3.put_object(Bucket=location_info.netloc, Key=output_path, Body=fileobj)
    else:
        raise RuntimeError("File storage format is unknown")


def list_files(path):
    """Lists all files at a specific URI

    Args:
        path (str): Directory or bucket URI containing the files to list.

    Raises:
        RuntimeError: If the path URI does not begin with 'file' or 's3'
        there is no handler for it yet.

    Returns:
        list: a list of strings that represent the full URI paths of each file
        in the directory/bucket.
    """
    location_info = urlparse(path)
    if location_info.scheme.lower() == "file":
        return os.listdir(location_info.path)
    if location_info.scheme.lower() == "s3":
        s3_list = s3.list_objects(
            Bucket=location_info.netloc, Marker=location_info.path
        )
        s3_contents = s3_list["Contents"]
        final_file_list = []
        for content in s3_contents:
            filename = content["Key"]
            final_file_list.append(f"{location_info.path}/{filename}")

        return final_file_list
    raise RuntimeError("File storage format is unknown")


async def stream_csv_from_data_paths(data_paths, wide_format=False):
    """Function to asynchronously stream parquet + csv files from
    a datapaths list

    Args:
        data_paths (List): List of string URIs representing files to grab.
        wide_format (boolean, optional): Boolean flag determing whether
        the data is returned long or wide. Defaults to False.

    Yields:
        streamable: Streamable file object to be returned via
        StreamingResponse
    """
    # Build single dataframe
    dataframe = pandas.concat(pandas.read_parquet(file) for file in data_paths)

    # Ensure pandas floats are used because vanilla python ones are problematic
    dataframe = dataframe.fillna("").astype(
        {
            col: "str"
            for col in dataframe.select_dtypes(include=["float32", "float64"]).columns
        },
        # Note: This links it to the previous `dataframe` so not a full copy
        copy=False,
    )
    if wide_format:
        dataframe_wide = pandas.pivot(
            dataframe, index=None, columns="feature", values="value"
        )  # Reshape from long to wide
        dataframe = dataframe.drop(["feature", "value"], axis=1)
        dataframe = pandas.merge(
            dataframe, dataframe_wide, left_index=True, right_index=True
        )

    # Prepare for writing CSV to a temporary buffer
    buffer = StringIO()
    writer = csv.writer(buffer)

    # Write out the header row
    writer.writerow(dataframe.columns)

    yield buffer.getvalue()
    buffer.seek(0)  # To clear the buffer we need to seek back to the start and truncate
    buffer.truncate()

    # Iterate over dataframe tuples, writing each one out as a CSV line one at a time
    for record in dataframe.itertuples(index=False, name=None):
        writer.writerow(str(i) for i in record)
        yield buffer.getvalue()
        buffer.seek(0)
        buffer.truncate()
