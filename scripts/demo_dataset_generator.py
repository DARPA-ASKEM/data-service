"""Script to populate a mock datasets in TDS
based on biomodel simulation output 'sim_output.json'
"""

import glob
import json

import requests

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


def create_dataset(maintainer_id, num_of_states, dataset_index):
    """Creates a demo dataset using a maintainer_id and number of states.

    Args:
        dataset_id (int): related dataset's id in postgres
        index (int): state number from dataset

    Returns:
        json: requests response in json format
    """
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
        "data_paths": [
            f"file:///datasets/{dataset_index}/{dataset_index}.parquet.gzip"
        ],
    }

    dataset_payload = {
        "name": f"Biomodel simulation output {dataset_index}",
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

    headers = {"Content-Type": "application/json"}

    dataset_response = requests.post(
        URL + "datasets", headers=headers, data=json.dumps(dataset_payload), timeout=100
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


# Main function


def programatically_populate_datasets():
    """Populates demonstration data into the datasets, features, and
    qualifiers tables.
    """
    folders = glob.glob("experiments-main/thin-thread-examples/biomodels/BIOMD*/")

    folder_index = 0
    for folder in folders:
        try:
            with open(folder + "sim_output.json", "r", encoding="utf-8") as sim_out:
                simulation_output = json.load(sim_out)
                states = simulation_output["states"]
                first_state_obj = states[0]
                num_of_states = len(first_state_obj)

                dataset_response = create_dataset(1, num_of_states, folder_index)
                dataset_id = dataset_response["id"]
                for state in range(num_of_states):
                    create_feature(dataset_id, state)
                create_qualifier(dataset_id, num_of_states)
        except FileNotFoundError:
            print("sim_output.json not found in " + folder)
        folder_index += 1
