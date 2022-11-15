"""
utils.download - functions that assist in converting a parquet file from
S3/local storage to a CSV and streaming it as a response
"""

import csv
from io import StringIO
from zlib import compressobj

import pandas as pd


async def stream_csv_from_data_paths(data_paths):
    """
    Function to take a parquet file, convert it to a csv,
    and write it to a buffer.
    """
    # Build single dataframe
    dataframe = pd.concat(pd.read_parquet(file) for file in data_paths)

    # Ensure pandas floats are used because vanilla python ones are problematic
    dataframe = dataframe.fillna("").astype(
        {
            col: "str"
            for col in dataframe.select_dtypes(include=["float32", "float64"]).columns
        },
        # Note: This links it to the previous `dataframe` so not a full copy
        copy=False,
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


async def compress_stream(content):
    """
    Compress stream function for browsers that
    request a compressed data stream.
    """
    compressor = compressobj()
    async for buff in content:
        yield compressor.compress(buff.encode())
    yield compressor.flush()
