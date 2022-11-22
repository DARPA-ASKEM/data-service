"""Script to populate a mock datasets in TDS
based on biomodel simulation output 'sim_output.json'
"""

import glob
import json

import requests
from json_to_csv import convert_biomd_json_to_csv

URL = "http://localhost:8001/"

# Function definitions


# def create_person():
#     """Creates a demo person in postgres

#     Returns:
#         json: requests response in json format
#     """
#     person_payload = {
#         "name": "Adam Smith",
#         "email": "Adam@test.io",
#         "org": "Uncharted",
#         "website": "",
#         "is_registered": True,
#     }

#     persons_response = requests.post(URL + "persons", json=person_payload, timeout=100)

#     p_response_obj = persons_response.json()

#     return p_response_obj
url = "http://localhost:8001/"


def asset_to_project(project_id, asset_id, asset_type):
    payload = json.dumps(
        {
            "project_id": project_id,
            "resource_id": asset_id,
            "resource_type": asset_type,
            "external_ref": "string",
        }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request(
        "POST",
        url + f"projects/{project_id}/assets/{asset_type}/{asset_id}",
        headers=headers,
        data=payload,
    )


def create_dataset(maintainer_id, num_of_states):
    """Creates a demo dataset using a maintainer_id and number of states.

    Args:
        maintainer_id (int): id of the maintainer linked to dataset
        num_of_states (int): state number from raw data

    Returns:
        json: requests response in json format
    """

    # Post dataset first to get ID from postgres
    headers = {"Content-Type": "application/json"}
    initial_dataset_payload = {
        "name": "Biomodel simulation output",
        "url": "",
        "description": "Biomodel simulation output registered as a dataset",
        "maintainer": maintainer_id,
    }

    initial_dataset_response = requests.post(
        URL + "datasets",
        headers=headers,
        data=json.dumps(initial_dataset_payload),
        timeout=100,
    )
    dataset_id = initial_dataset_response.json()["id"]
    print(dataset_id)

    feature_array = []
    for state in range(num_of_states):
        feature_dict = {
            "name": f"state_{state}",
            "display_name": "",
            "description": f"state feature {state}",
            "type": "feature",
            "feature_type": "float",
            "units": "na",
            "units_description": "",
            "qualifies": [],
            "primary_ontology_id": "",
            "qualifierrole": "breakdown",
            "aliases": {},
        }
        feature_array.append(feature_dict)

    qualifies_array = []
    for state in range(num_of_states):
        qualifies_array.append(f"state_{state}")

    time_step_qual = {
        "name": "time",
        "display_name": "",
        "description": "time step feature",
        "type": "feature",
        "feature_type": "float",
        "units": "na",
        "units_description": "",
        "qualifies": qualifies_array,
        "primary_ontology_id": "",
        "qualifierrole": "breakdown",
        "aliases": {},
    }

    feature_array.append(time_step_qual)

    data_path_string = f"file:///datasets/{dataset_id}/sim_output.csv"

    annotation = {
        "annotations": {
            "geo": [
                {
                    "name": "mock_lon",
                    "display_name": "loc",
                    "description": "location",
                    "type": "geo",
                    "geo_type": "longitude",
                    "primary_geo": True,
                    "resolve_to_gadm": False,
                    "coord_format": "lonlat",
                    "qualifies": [],
                    "aliases": {},
                    "gadm_level": "admin1",
                },
                {
                    "name": "mock_lat",
                    "display_name": "loc",
                    "description": "location",
                    "type": "geo",
                    "geo_type": "latitude",
                    "primary_geo": True,
                    "resolve_to_gadm": False,
                    "is_geo_pair": "mock_lon",
                    "coord_format": "lonlat",
                    "qualifies": [],
                    "aliases": {},
                    "gadm_level": "admin1",
                },
            ],
            "date": [
                {
                    "name": "mock_time",
                    "display_name": "",
                    "description": "date",
                    "type": "date",
                    "date_type": "date",
                    "primary_date": True,
                    "time_format": "%m/%d/%Y",
                    "qualifies": [],
                    "aliases": {},
                }
            ],
            "feature": feature_array,
        },
        "data_paths": [data_path_string],
    }

    dataset_payload = {
        "name": f"Biomodel simulation output {dataset_id}",
        "url": "",
        "description": "Biomodel simulation output registered as a dataset",
        "deprecated": False,
        "sensitivity": "",
        "quality": "Measured",
        "temporal_resolution": "",
        "geospatial_resolution": "",
        "annotations": json.dumps(annotation),
        "maintainer": maintainer_id,
    }

    dataset_response = requests.patch(
        URL + f"datasets/{dataset_id}",
        headers=headers,
        data=json.dumps(dataset_payload),
        timeout=100,
    )
    print(f"Dataset post response: {dataset_response}")

    dataset_json = dataset_response.json()

    return dataset_json


def create_feature(dataset_id, index):
    """Creates a demo feature using a dataset_id and a feature index.

    Args:
        dataset_id (int): related dataset's id in postgres
        index (int): state number from dataset

    Returns:
        json: requests response in json format
    """
    feature_payload = {
        "dataset_id": dataset_id,
        "description": f"State Feature {index}",
        "display_name": f"state_{index}",
        "name": f"state_{index}",
        "value_type": "float",
    }
    feature_response = requests.post(
        URL + "datasets/features",
        json=feature_payload,
        timeout=100,
    )

    return feature_response.json()


def create_qualifier(dataset_id, num_of_states):
    """Creates a demo qualifier using a dataset_id and number of states.

    Args:
        dataset_id (int): related dataset's id in postgres
        num_of_states (int): number of states in sample data

    Returns:
        json: requests response in json format
    """
    qualifier_payload = {
        "dataset_id": dataset_id,
        "description": "Timestep feature qualifier",
        "display_name": "timestep_qualifier",
        "name": "timestep_qualifier",
        "value_type": "float",
    }
    qualifies_array = []
    for state in range(num_of_states):
        qualifies_array.append(f"state_{state}")
    qualifier_full_payload = {
        "payload": qualifier_payload,
        "qualifies_array": qualifies_array,
    }

    qualifier_response = requests.post(
        URL + "datasets/qualifiers",
        json=qualifier_full_payload,
        timeout=100,
    )

    return qualifier_response.json()


def upload_file_to_tds(id, file_object):
    """Uploads a file_object to TDS

    Args:
        id (int): dataset id the file is associated with
        file_object (file): file to upload

    Returns:
        json: Requests response in json format
    """

    payload = {"id": id}
    file_payload = {"file": file_object}
    upload_response = requests.post(
        URL + f"datasets/{id}/upload/file",
        files=file_payload,
        json=payload,
        timeout=100,
    )

    return upload_response.json()


# Main function


def programatically_populate_datasets():
    """Populates demonstration data into the datasets, features, and
    qualifiers tables.
    """
    folders = glob.glob("experiments-main/thin-thread-examples/biomodels/BIOMD*/")

    for folder in folders:
        try:
            # Open json to get relevant information
            with open(folder + "sim_output.json", "r", encoding="utf-8") as sim_out:
                simulation_output = json.load(sim_out)
                states = simulation_output["states"]
                first_state_obj = states[0]
                num_of_states = len(first_state_obj)

                # Create the dataset with maintainer_id of 1
                # assuming the first maintainer is already created.
                dataset_response = create_dataset(
                    maintainer_id=1,
                    num_of_states=num_of_states,
                )
                dataset_id = dataset_response["id"]
                # Convert the json to a CSV
                convert_biomd_json_to_csv(
                    json_file_path=folder + "sim_output.json",
                    output_file_path=folder + "sim_output.csv",
                )
                # Upload the CSV to TDS for full mock data
                with open(folder + "sim_output.csv", "rb") as sim_csv:
                    print(f"Uploading file to dataset_id {dataset_id}")
                    upload_file_to_tds(id=dataset_id, file_object=sim_csv)
                    print(dataset_id)
                # Finish populating dataset metadata: Features, Qualifiers
                for state in range(num_of_states):
                    create_feature(dataset_id, state)
                create_qualifier(dataset_id, num_of_states)
                asset_to_project(1, dataset_id, "datasets")

        except FileNotFoundError:
            print("sim_output.json not found in " + folder)
