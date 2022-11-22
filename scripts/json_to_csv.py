"""
Script to convert ASKEM simulation output .json to .csv for
data-annotation processing.
"""

import csv
import json
import sys


def convert_biomd_json_to_csv(json_file_path, output_file_path):
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

            headers = [
                "timestamp, country, admin1, admin2, admin3, lat, lng, feature, value"
            ]

            # Write header wrote
            csv_writer.writerow(headers)

            # Write all states out as their own row.
            for list_index in range(len(states)):
                timestamp = times[list_index]
                for state in states[list_index]:
                    value_index = states[list_index].index(state)
                    row = [
                        timestamp,
                        None,
                        None,
                        None,
                        None,
                        "0.1",
                        "1.0",
                        f"state_{value_index}",
                        state,
                    ]
                    csv_writer.writerow(row)


if __name__ == "__main__":
    convert_biomd_json_to_csv(sys.argv[1], sys.argv[2])
