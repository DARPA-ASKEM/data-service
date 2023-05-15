import json
import os
from glob import glob
from io import BytesIO
from tempfile import TemporaryDirectory
from urllib.request import urlopen
from zipfile import ZipFile

import requests

REPO = "https://github.com/DARPA-ASKEM/experiments/archive/refs/heads/main.zip"  # TODO(five): Pin rev
URL = "http://localhost:8001/"  # TODO(five): Handle non-leading `/` case
MODELS_SUBDIR_PATH = "experiments-main/thin-thread-examples/mira_v2/biomodels/"
MODEL_DIR_PATTERN = "BIO*"
MODEL_CONCEPTS = "model_mmt_templates.json"
DOCUMENT_ID = "document_xdd_gddid.txt"
MODEL = "model_askenet.json"
XDD_MAPPINGS = "scripts/xdd_mapping.json"
DATASETS_SUBDIR_PATH = "experiments-main/thin-thread-examples/exemplar_datasets/"
DATASET_DIR_PATTERN = "*"
DATASET_METADATA = "meta.json"


def create_asset(route, payload, url) -> int | None:
    headers = {"Content-Type": "application/json"}
    response = requests.request(
        "POST", f"{url}{route}", headers=headers, data=json.dumps(payload)
    )
    response.raise_for_status()
    response_data = response.json()
    if "id" in response_data:
        asset_id = response_data.get("id")
        return asset_id


def attach_to_project(asset_id, asset_type, project_id, url):
    response = requests.post(
        f"{url}projects/{project_id}/assets/{asset_type}/{asset_id}"
    )
    response.raise_for_status()


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


def list_asset_dirs(root_path, subdir, pattern) -> list[str]:
    full_path = os.path.join(root_path, subdir)
    return sorted(glob(full_path + pattern))


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


def create_models(
    root_path,
    url,
    necessary_entities,
    models_subdir=MODELS_SUBDIR_PATH,
    model_dir_pattern=MODEL_DIR_PATTERN,
    model_file=MODEL,
    document_id_path=DOCUMENT_ID,
    xdd_mappings_filepath=XDD_MAPPINGS,
):
    """
    Create all the datasets listed in the directory
    """
    with open(xdd_mappings_filepath, "r") as file:
        uri_to_title_mappings = json.load(file)
    for model_dir in list_asset_dirs(root_path, models_subdir, model_dir_pattern):
        print(f"Working on {model_dir}..")
        with open(os.path.join(model_dir, document_id_path), "r") as file:
            xdd_uri = file.read()
        publication_payload = {
            "xdd_uri": xdd_uri,
            "title": uri_to_title_mappings.get(xdd_uri, "Unknown"),
        }
        publication_id = create_asset("external/publications", publication_payload, url)
        attach_to_project(
            publication_id, "publications", necessary_entities["projects"], url
        )
        print(f"\tCreated publication with id: {publication_id}")
        with open(os.path.join(model_dir, model_file), "r") as file:
            raw_model = file.read()
        model = json.loads(raw_model)
        model_payload = {
            "name": model["name"],
            "description": model["description"],
            "content": raw_model,
            "framework": "petrinet",  # TODO(five): Dynamically select framework in the future OR have tds figure it out
        }
        model_id = create_asset("models", model_payload, url)
        attach_to_project(model_id, "models", necessary_entities["projects"], url)
        print(f"\tCreated model with id: {model_id}")
        # TODO(five): Add optional `publication` parameter to model post endpoint itself that handles provenance
        # TODO(five): This is broken because intermediates have been removed and models don't connect to publications
        connect_through_provenance(
            model_id,
            "Model",
            publication_id,
            "Publication",
            "EXTRACTED_FROM",
            necessary_entities["persons"],
            url=url,
        )
        # TODO(five): Attach parameters? should be included in content
        # TODO(five): Attach concepts? should be included in content


def create_datasets(
    root_path,
    url,
    necessary_entities,
    dataset_subdir=DATASETS_SUBDIR_PATH,
    dataset_dir_pattern=DATASET_DIR_PATTERN,
    metadata_file=DATASET_METADATA,
):
    """
    Create all the models listed in the directory
    """
    for dataset_dir in list_asset_dirs(root_path, dataset_subdir, dataset_dir_pattern):
        with open(os.path.join(dataset_dir, metadata_file), "r") as file:
            metadata = json.load(file)

        dataset_metadata_payload = {
            "name": metadata["name"],
            "url": metadata["maintainer"]["website"],
            "description": metadata["description"],
            "maintainer": necessary_entities["persons"],
        }
        dataset_id = create_asset("datasets", dataset_metadata_payload, url)
        attach_to_project(dataset_id, "datasets", necessary_entities["projects"], url)

        with open(glob(os.path.join(dataset_dir, "*.parquet.gzip"))[0], "rb") as file:
            upload_response = requests.post(
                URL + f"datasets/{dataset_id}/files",
                files={"file": file},
                timeout=100,
            )
            upload_response.raise_for_status()

        curies = set()
        for feature in metadata["outputs"]:
            if feature["primaryOntologyId"]:
                curies.add(feature["primaryOntologyId"])
        for curie in curies:
            concept_payload = {
                "curie": curie,
                "type": "datasets",
                "object_id": dataset_id,
                "status": "obj",
            }
            create_asset("concepts", concept_payload, url)
        print(f"Created dataset with id: {dataset_id}")
        # TODO(five): Upload features and qualifiers. Do we still want features??


def populate(repo=REPO, tds_url=URL):
    """
    Populate TDS using data from the experiments repo
    """
    http_response = urlopen(repo)
    with TemporaryDirectory() as tmp_dir:
        tmp_path = str(tmp_dir)
        zipfile = ZipFile(BytesIO(http_response.read()))
        zipfile.extractall(tmp_path)

        dependencies = create_dependency_entities(tds_url)
        print("Placeholder data created.")
        # create_models(tmp_path, tds_url, dependencies)
        create_datasets(tmp_path, tds_url, dependencies)
    print("Population is complete!")


if __name__ == "__main__":
    populate()
