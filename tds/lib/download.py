import csv
from io import StringIO
from zlib import compressobj

import pandas as pd


async def stream_csv_from_data_paths(data_paths):
    # Build single dataframe
    df = pd.concat(pd.read_parquet(file) for file in data_paths)

    # Ensure pandas floats are used because vanilla python ones are problematic
    df = df.fillna("").astype(
        {
            col: "str"
            for col in df.select_dtypes(include=["float32", "float64"]).columns
        },
        # Note: This links it to the previous `df` so not a full copy
        copy=False,
    )

    # Prepare for writing CSV to a temporary buffer
    buffer = StringIO()
    writer = csv.writer(buffer)

    # Write out the header row
    writer.writerow(df.columns)

    yield buffer.getvalue()
    buffer.seek(0)  # To clear the buffer we need to seek back to the start and truncate
    buffer.truncate()

    # Iterate over dataframe tuples, writing each one out as a CSV line one at a time
    for record in df.itertuples(index=False, name=None):
        writer.writerow(str(i) for i in record)
        yield buffer.getvalue()
        buffer.seek(0)
        buffer.truncate()


async def compress_stream(content):
    compressor = compressobj()
    async for buff in content:
        yield compressor.compress(buff.encode())
    yield compressor.flush()
