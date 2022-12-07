"""
Script to convert ASKEM simulation output .json to .csv for
data-annotation processing.
"""

import csv
import json
import sys


def convert_sim_runs_to_csv(json_file_path, output_file_path):
    """
    Converts ASKEM simulation output.json to CSV

    Args:
        json_file_path (str): input .json filepath
        output_file_path (str): output .csv filepath
    """

    with open(json_file_path, encoding="utf-8") as json_file:
        jsondata = json.load(json_file)
        times = jsondata.pop("_time")
        time_values = times["value"]

        with open(output_file_path, "w", newline="", encoding="utf-8") as data_file:

            csv_writer = csv.writer(data_file)

            headers = [
                "timestamp",
                "country",
                "admin1",
                "admin2",
                "admin3",
                "lat",
                "lng",
                "feature",
                "value",
            ]

            # Write header wrote
            csv_writer.writerow(headers)

            # Write all states out as their own row.
            for feature_object in list(jsondata.values()):
                values_list = feature_object["value"]
                feature_name = feature_object["name"]
                for list_index in range(len(time_values)):
                    timestamp = time_values[list_index]
                    feature_value = values_list[list_index]
                    row = [
                        timestamp,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        feature_name,
                        feature_value,
                    ]
                    csv_writer.writerow(row)


if __name__ == "__main__":
    convert_sim_runs_to_csv(sys.argv[1], sys.argv[2])
