"""Script to populate a mock datasets in TDS
based on biomodel simulation output 'sim_output.json'
"""

import json

import requests


## Dataset code ###
def create_dataset(
    maintainer_id,
    dataset_object,
    url="http://localhost:8001",
    biomodel_name=None,
    biomodel_description=None,
    simulation_run=True,
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
        "simulation_run": simulation_run,
    }

    initial_dataset_response = requests.post(
        url + "datasets",
        headers=headers,
        data=json.dumps(initial_dataset_payload),
        timeout=100,
    )
    dataset_id = initial_dataset_response.json()["id"]

    feature_array = []
    qualifies_array = []
    for feature in list(dataset_object.values()):
        name = feature["name"]
        if name == "_time":
            continue
        feature_context = feature["context"]
        ontology = None
        try:
            ontology = feature_context["property"]
        except KeyError:
            ontology = ""
        feature_dict = {
            "name": name,
            "display_name": "",
            "description": f"{name} state feature",
            "type": "feature",
            "feature_type": "float",
            "units": "na",
            "units_description": "",
            "qualifies": [],
            "primary_ontology_id": ontology,
            "qualifierrole": "breakdown",
            "aliases": {},
        }
        feature_array.append(feature_dict)
        qualifies_array.append(name)

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
        "name": f"{biomodel_name}",
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
    feature_obj,
    url="http://localhost:8001/",
):
    """Creates a demo feature using a dataset_id and a feature index.

    Args:
        dataset_id (int): related dataset's id in postgres
        index (int): state number from dataset

    Returns:
        json: requests response in json format
    """
    name = feature_obj["name"]
    feature_payload = {
        "dataset_id": dataset_id,
        "description": f"{name} state feature",
        "display_name": name,
        "name": name,
        "value_type": "float",
    }
    feature_response = requests.post(
        url + "datasets/features",
        json=feature_payload,
        timeout=100,
    )

    response_json = feature_response.json()
    feature_id = response_json["id"]
    try:
        curie = feature_obj["context"]
        curie = curie["property"]
        create_concept(feature_id, "features", curie)
    except KeyError:
        pass

    return response_json


def create_qualifier(dataset_id, dataset_object, url="http://localhost:8001/"):
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
    for name in dataset_object.keys():
        qualifies_array.append(name)
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


def create_concept(object_id, type, curie, status="obj", url="http://localhost:8001/"):

    concept_payload = {
        "curie": curie,
        "type": type,
        "object_id": object_id,
        "status": status,
    }

    concept_response = requests.post(
        url + "concepts",
        json=concept_payload,
        timeout=100,
    )

    return concept_response.json()


def upload_file_to_tds(id, file_object, url="http://localhost:8001/"):
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
