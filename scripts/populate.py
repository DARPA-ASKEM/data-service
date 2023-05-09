import json
import os
from glob import glob
from io import BytesIO
from tempfile import TemporaryDirectory
from urllib.request import urlopen
from zipfile import ZipFile

import requests

REPO = "https://github.com/DARPA-ASKEM/experiments/archive/refs/heads/main.zip"  # TODO(five): Pin rev
MODELS_SUBDIR_PATH = "thin-thread-examples/mira_v2/biomodels"
URL = "http://localhost:8001"
XDD_MAPPINGS = "scripts/xdd_mapping.json"
DOCUMENT_ID = "document_xdd_gddid.txt"
MODEL_CONCEPTS = "model_mmt_templates.json"
MODEL = "model_askenet.json"


def collect_model_concepts(model_dir, filename=MODEL_CONCEPTS):
    model_concepts = []
    with open(os.path.join(model_dir, filename), "r") as f:
        mmt_template = json.load(f)

    for template in mmt_template.get("templates"):
        for key in template:
            if key == "subject" or key == "outcome":
                for identifier in template[key].get("identifiers"):
                    if not "biomodels" in identifier:
                        model_concepts.append(
                            f"{identifier}:{template[key].get('identifiers').get(identifier)}"
                        )
            elif key == "controllers":
                for controller in template[key]:
                    for identifier in controller.get("identifiers"):
                        if "biomodels" not in identifier:
                            model_concepts.append(
                                f"{identifier}:{controller.get('identifiers').get(identifier)}"
                            )
                    for identifier in controller.get("context"):
                        model_concepts.append(
                            f"{identifier}:{controller.get('identifiers').get(identifier)}"
                        )
    return [*set(model_concepts)]


def create_asset(route, payload, url) -> int | None:
    headers = {"Content-Type": "application/json"}
    response = requests.request(
        "POST", f"{url}{route}", headers=headers, data=json.dumps(payload)
    )
    response_data = response.json()
    if "id" in response_data:
        asset_id = response_data.get("id")
        return asset_id


def attach_to_project(asset_id, asset_type, project_id, url):
    payload = {
        "project_id": project_id,
        "resource_id": asset_id,
        "resource_type": asset_type,
        "external_ref": "string",
    }
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
    payload = {
        "left": left_id,
        "left_type": left_type,
        "right": right_id,
        "right_type": right_type,
        "relation_type": relation_type,
        "user_id": user_id,
        "concept": concept,  # NOTE: this seems to be for caching, making searches easier later
    }
    create_asset(f"provenance", payload, url)


def attach_to_concept(concept, object_id, object_type, url):
    payload = {
        "curie": concept,
        "type": object_type,
        "object_id": object_id,
        "status": "obj",
    }
    create_asset(f"concepts", payload, url)
    # TODO(five): Do we want to add provenance manually??


def create_dependency_entities(url) -> dict[str, int | None]:
    """
    Create entities that are necessary to create other entities. This
    data does NOT come from upstream, it's just placeholder data
    to make sure stuff works
    """
    payloads = {
        "persons": {
            "name": "Adam Smith",
            "email": "Adam@test.io",
            "org": "Uncharted",
            "website": "",
            "is_registered": True,
        },
        "projects": {
            "name": "My Project",
            "description": "First project in TDS",
            "assets": {},
            "status": "active",
            "username": "Adam Smith",
        },
        "models/frameworks": {
            "name": "petrinet",
            "version": "0.0.1",  # TODO(five): Are MRs versioned?
            "semantics": "semantics_go_here",  # TODO(five): Add petrinet schema in once they're used for validation
        },
    }
    return {
        route: create_asset(route, payload, url) for route, payload in payloads.items()
    }


def create_models(path, url, necessary_entities, xdd_mappings_filepath=XDD_MAPPINGS):
    """
    Create all the datasets listed in the directory
    """
    full_model_path = os.path.join(path, MODELS_SUBDIR_PATH)
    model_dirs = sorted(glob(full_model_path + "/*/"))
    with open(xdd_mappings_filepath, "r") as file:
        uri_to_title_mappings = json.load(file)
    for model_dir in model_dirs:
        print(f"Working on {model_dir}")
        with open(os.path.join(model_dir, DOCUMENT_ID), "r") as file:
            xdd_uri = file.read()
        publication_payload = {
            "xdd_uri": xdd_uri,
            "title": uri_to_title_mappings.get(xdd_uri, "Unknown"),
        }
        publication_id = create_asset("/publications", publication_payload, url)
        print(f"Created publication with id: {id}")
        with open(os.path.join(model_dir, MODEL), "r") as file:
            raw_model = file.read()
        model = json.loads(raw_model)
        model_payload = {
            "name": model["name"],
            "description": model["description"],
            "content": raw_model,
            "framework": necessary_entities["models/frameworks"],
        }
        model_id = create_asset("/models", model_payload, url)
        print(f"Created model with id: {id}")
        # TODO(five): Add optional `publication` parameter to model post that handles provenance
        connect_through_provenance(
            model_id,
            "Model",
            publication_id,
            "Publication",
            "EXTRACTED_FROM",
            necessary_entities["persons"],
            url=url,
        )
        # TODO(five): Attach parameters
        # TODO(five): Attach concepts


def create_datasets(path, url):
    """
    Create all the models listed in the directory
    """
    # TODO(five): Iterate over every directory
    # TODO(five): Upload dataset
    # TODO(five): Attch concepts


def populate(url=URL):
    """
    Populate TDS using data from the experiments repo
    """
    http_response = urlopen(url)
    with TemporaryDirectory() as tmp_dir:
        tmp_path = str(tmp_dir)
        zipfile = ZipFile(BytesIO(http_response.read()))
        zipfile.extractall(tmp_path)

        dependencies = create_dependency_entities(url)
        print("Placeholder data created.")
        create_models(tmp_path, dependencies, url)
        create_datasets(tmp_path, url)
    print("Population is complete!")
