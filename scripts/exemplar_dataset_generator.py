"""Script to populate a mock datasets in TDS
based on exemplar datasets from askem-demo.dojo-modeling.com
"""

import glob
import json

import requests

URL = "http://localhost:8001/"


# Function definitions


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
        URL + f"projects/{project_id}/assets/{asset_type}/{asset_id}",
        headers=headers,
        data=payload,
    )


def create_dataset(maintainer_id, meta_object):
    """Creates a demo dataset using a maintainer_id and number of states.

    Args:
        maintainer_id (int): id of the maintainer linked to dataset
        meta_object (Dict): dictionary of metadata about dataset.

    Returns:
        json: requests response in json format
    """

    # Post dataset first to get ID from postgres
    headers = {"Content-Type": "application/json"}
    initial_dataset_payload = {
        "name": meta_object["name"],
        "url": meta_object["maintainer"]["website"],
        "description": meta_object["description"],
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

    data_path_list = []
    for data_path in meta_object["data_paths"]:
        file_name = data_path.split("/")[-1]
        data_path_string = f"s3://datasets/{dataset_id}/{file_name}"
        data_path_list.append(data_path_string)

    annotation = {
        "annotations": {},
        "data_paths": data_path_list,
    }

    dataset_payload = {
        "name": meta_object["name"],
        "url": meta_object["maintainer"]["website"],
        "description": meta_object["description"],
        "deprecated": False,
        "sensitivity": meta_object["data_sensitivity"],
        "quality": meta_object["data_quality"],
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


def create_feature(dataset_id, feature_obj):
    """Creates a demo feature using a dataset_id and a feature index.

    Args:
        dataset_id (int): related dataset's id in postgres
        feature_obj (Dict): dictionary of feature data.

    Returns:
        json: requests response in json format
    """
    feature_payload = {
        "dataset_id": dataset_id,
        "description": feature_obj["description"],
        "display_name": feature_obj["display_name"],
        "name": feature_obj["name"],
        "value_type": feature_obj["type"],
    }
    feature_response = requests.post(
        URL + "datasets/features",
        json=feature_payload,
        timeout=100,
    )

    return feature_response.json()


def create_qualifier(dataset_id, qualifier_obj):
    """Creates a demo qualifier using a dataset_id and number of states.

    Args:
        dataset_id (int): related dataset's id in postgres
        qualifier_obj (Dict): dictionary of qualifier data.

    Returns:
        json: requests response in json format
    """
    # Check the value type to make sure it conforms.
    value_type = "str"
    qualifier_type = qualifier_obj["type"]
    accepted_value_types = {"binary", "bool", "float", "int", "str"}
    if qualifier_type in accepted_value_types:
        value_type = qualifier_type

    # Now construct payload
    qualifier_payload = {
        "dataset_id": dataset_id,
        "description": qualifier_obj["description"],
        "display_name": qualifier_obj["display_name"],
        "name": qualifier_obj["name"],
        "value_type": value_type,
    }
    # Construct full payload with additional qualifies list.
    qualifies_array = qualifier_obj["related_features"]
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


def create_concept(object_id, type, curie, status="obj"):

    concept_payload = {
        "curie": curie,
        "type": type,
        "object_id": object_id,
        "status": status,
    }

    concept_response = requests.post(
        URL + "concepts",
        json=concept_payload,
        timeout=100,
    )

    return concept_response.json()


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


def populate_exemplar_datasets():
    """Populates demonstration exemplar data into the datasets, features, and
    qualifiers tables.
    """
    folders = glob.glob("experiments-main/thin-thread-examples/exemplar_datasets/*/")

    for folder in sorted(folders):
        print(folder)
        try:
            # Open json to get relevant information
            with open(folder + "meta.json", "r", encoding="utf-8") as meta:
                meta_object = json.load(meta)
                features = meta_object["outputs"]
                qualifiers = meta_object["qualifier_outputs"]

                # Create the dataset with maintainer_id of 1
                # assuming the first maintainer is already created.
                dataset_response = create_dataset(
                    maintainer_id=1, meta_object=meta_object
                )
                dataset_id = dataset_response["id"]
                file_to_upload = glob.glob(folder + "*.parquet.gzip")
                # Upload the CSV to TDS for full mock data
                for file in file_to_upload:
                    with open(file, "rb") as exemplar_parquet:
                        print(f"Uploading file to dataset_id {dataset_id}")
                        upload_file_to_tds(id=dataset_id, file_object=exemplar_parquet)
                        print(dataset_id)
                # Finish populating dataset metadata: Features, Qualifiers
                list_of_curies = []
                for feature_object in features:
                    feature_response = create_feature(dataset_id, feature_object)
                    feature_id = feature_response["id"]
                    if feature_object["primaryOntologyId"]:
                        list_of_curies.append(feature_object["primaryOntologyId"])
                        create_concept(
                            object_id=feature_id,
                            type="features",
                            curie=feature_object["primaryOntologyId"],
                        )
                unique_curies = [*set(list_of_curies)]
                for curie in unique_curies:
                    create_concept(object_id=dataset_id, type="datasets", curie=curie)
                for qualifier_object in qualifiers:
                    create_qualifier(dataset_id, qualifier_object)
                asset_to_project(1, dataset_id, "datasets")

        except FileNotFoundError:
            print("meta.json not found in " + folder)
