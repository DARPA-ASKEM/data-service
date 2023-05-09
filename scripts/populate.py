from io import BytesIO
from json import dumps
from tempfile import TemporaryDirectory
from urllib.request import urlopen
from zipfile import ZipFile

import requests


def create(route, payload, url) -> int | None:
    headers = {"Content-Type": "application/json"}

    # return resource_id (a1)
    response = requests.request("POST", f"{url}{route}", headers=headers, data=payload)

    response_data = response.json()
    if "id" in response_data:
        publication_id = response_data.get("id")
        return publication_id
    else:
        return


def create_dependency_entities(dir, url) -> dict[str, int | None]:
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
    return {route: create(route, payload, url) for route, payload in payloads.items()}


def create_models(dir, url):
    """
    Create all the datasets listed in the directory
    """
    # TODO(five): Iterate over every directory
    # TODO(five): Upload paper
    # TODO(five): Upload model


def attach_concepts(dir, url):
    """
    Attach concepts to datasets, models, parameters, etc
    """
    # TODO(five): Attach a concept to each entity


def create_datasets(dir, url):
    """
    Create all the models listed in the directory
    """
    # TODO(five): Iterate over every directory
    # TODO(five): Upload dataset


def populate():
    """
    Populate TDS using data from the experiments repo
    """
    url = "http://localhost:8000/"
    http_response = urlopen(url)
    with TemporaryDirectory() as temp_dir:
        # Download and extract experiments repo
        zipfile = ZipFile(BytesIO(http_response.read()))
        zipfile.extractall(str(temp_dir))

        # Populate data
        create_dependency_entities(temp_dir, url)
        create_models(temp_dir, url)
        create_datasets(temp_dir, url)
    print("Population is complete")
