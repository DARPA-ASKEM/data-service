import os
from glob import glob
from io import BytesIO
from json import dumps
from tempfile import TemporaryDirectory
from urllib.request import urlopen
from zipfile import ZipFile

import requests

REPO = "https://github.com/DARPA-ASKEM/experiments"  # TODO(five): Incorrect link
MODELS_SUBDIR_PATH = "thin-thread-examples/mira_v2/biomodels"
URL = "http://localhost:8001"


def create_asset(route, payload, url) -> int | None:
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", f"{url}{route}", headers=headers, data=payload)
    response_data = response.json()
    if "id" in response_data:
        asset_id = response_data.get("id")
        return asset_id
    else:
        return


def attach_to_project(asset_id, asset_type, project_id, url):
    payload = dumps(
        {
            "project_id": project_id,
            "resource_id": asset_id,
            "resource_type": asset_type,
            "external_ref": "string",
        }
    )
    create_asset(f"projects/{project_id}/assets/{asset_type}", payload, url)


def connect_through_provenance(
    left_id,
    left_type,
    right_id,
    right_type,
    relation_type,
    user_id,
    concept=".",
    url=URL,
):
    payload = dumps(
        {
            "left": left_id,
            "left_type": left_type,
            "right": right_id,
            "right_type": right_type,
            "relation_type": relation_type,
            "user_id": user_id,
            "concept": concept,  # NOTE: this seems to be for caching, making searches easier later
        }
    )
    create_asset(f"provenance", payload, url)


def attach_to_concept(concept, object_id, object_type, url):
    payload = dumps(
        {
            "curie": concept,
            "type": object_type,
            "object_id": object_id,
            "status": "obj",
        }
    )
    create_asset(f"concepts", payload, url)


def create_dependency_entities(url) -> dict[str, int | None]:
    """
    Create entities that are necessary to create other entities. This
    data does NOT come from upstream, it's just placeholder data
    to make sure stuff works
    """
    payloads = {
        "persons": dumps(
            {
                "name": "Adam Smith",
                "email": "Adam@test.io",
                "org": "Uncharted",
                "website": "",
                "is_registered": True,
            }
        ),
        "projects": dumps(
            {
                "name": "My Project",
                "description": "First project in TDS",
                "assets": {},
                "status": "active",
                "username": "Adam Smith",
            }
        ),
        "models/frameworks": dumps(
            {
                "name": "Petri Net",
                "version": "0.0.1",
                "semantics": "semantics_go_here",
            }
        ),
    }
    return {
        route: create_asset(route, payload, url) for route, payload in payloads.items()
    }


def create_models(path, url):
    """
    Create all the datasets listed in the directory
    """
    full_model_path = os.path.join(path, MODELS_SUBDIR_PATH)
    model_dirs = sorted(glob(full_model_path + "/*/"))

    # TODO(five): Iterate over every directory
    # TODO(five): Upload paper
    # TODO(five): Upload model


def create_datasets(path, url):
    """
    Create all the models listed in the directory
    """
    # TODO(five): Iterate over every directory
    # TODO(five): Upload dataset


def populate(url=URL):
    """
    Populate TDS using data from the experiments repo
    """
    http_response = urlopen(url)
    with TemporaryDirectory() as tmp_dir:
        tmp_path = str(tmp_dir)
        # Download and extract experiments repo
        zipfile = ZipFile(BytesIO(http_response.read()))
        zipfile.extractall(tmp_path)

        dependencies = create_dependency_entities(url)
        print("Placeholder data created.")

        create_models(tmp_path, url)
        create_datasets(tmp_path, url)
    print("Population is complete!")
