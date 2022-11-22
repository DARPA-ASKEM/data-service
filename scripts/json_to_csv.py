"""
Script to convert ASKEM simulation output .json to .csv for
data-annotation processing.
"""

import csv
import json
import sys


def convert_biomd_json_to_csv(json_file_path, output_file_path, mock_geo_time=True):
    """
    Converts ASKEM simulation output

    Args:
        json_file_path (str): input .json filepath
        output_file_path (str): output .csv filepath
    """

    with open(json_file_path, encoding="utf-8") as json_file:
        jsondata = json.load(json_file)
        states = jsondata["states"]
        times = jsondata["time"]

        with open(output_file_path, "w", newline="", encoding="utf-8") as data_file:

            csv_writer = csv.writer(data_file)

            headers = []
            state_length = len(states[0])  # Grabs len of first "row" of states

            # Use state_length to construct header row
            for state_suffix in range(state_length):
                headers.append(f"state_{state_suffix}")
            headers.append("time")
            if mock_geo_time:
                headers.append("mock_lat")
                headers.append("mock_lon")
                headers.append("mock_time")

            # Write header wrote
            csv_writer.writerow(headers)

            # Write all other rows
            # First add times to the state value matrix
            for list_index in range(len(states)):
                states[list_index].append(times[list_index])
                if mock_geo_time:
                    # Append mock lat, lon, time values
                    states[list_index].append("0.1")
                    states[list_index].append("1.0")
                    states[list_index].append("01/01/2020")
            csv_writer.writerows(states)


if __name__ == "__main__":
    convert_biomd_json_to_csv(sys.argv[1], sys.argv[2])
