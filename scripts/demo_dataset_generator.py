"""Script to populate a mock datasets in TDS
based on biomodel simulation output 'sim_output.json'
"""

import glob
import json

import requests
from json_to_csv import convert_biomd_json_to_csv


## Dataset code ###
def create_dataset(
    maintainer_id,
    num_of_states,
    url="http://localhost:8001",
    biomodel_name=None,
    biomodel_description=None,
):
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
        "name": f"Biomodel simulation output {biomodel_name}",
        "url": "",
        "description": biomodel_description,
        "maintainer": maintainer_id,
    }

    initial_dataset_response = requests.post(
        url + "datasets",
        headers=headers,
        data=json.dumps(initial_dataset_payload),
        timeout=100,
    )
    dataset_id = initial_dataset_response.json()["id"]

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
        "name": f"Biomodel simulation output {biomodel_name}",
        "url": "",
        "description": f"Dataset from simulation run output- Model description: {biomodel_description}",
        "deprecated": False,
        "sensitivity": "",
        "quality": "Measured",
        "temporal_resolution": "",
        "geospatial_resolution": "",
        "annotations": json.dumps(annotation),
        "maintainer": maintainer_id,
    }

    dataset_response = requests.patch(
        url + f"datasets/{dataset_id}",
        headers=headers,
        data=json.dumps(dataset_payload),
        timeout=100,
    )
    print(f"Dataset post response: {dataset_response}")

    dataset_json = dataset_response.json()

    return dataset_json


def create_feature(
    dataset_id,
    index,
    url="http://localhost:8001",
):
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
        url + "datasets/features",
        json=feature_payload,
        timeout=100,
    )

    return feature_response.json()


def create_qualifier(dataset_id, num_of_states, url="http://localhost:8001"):
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
        url + "datasets/qualifiers",
        json=qualifier_full_payload,
        timeout=100,
    )

    return qualifier_response.json()


def upload_file_to_tds(id, file_object, url="http://localhost:8001"):
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
        url + f"datasets/{id}/upload/file",
        files=file_payload,
        json=payload,
        timeout=100,
    )

    return upload_response.json()
