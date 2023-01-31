import json
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

import requests

url = "http://localhost:8001/"


def download_and_unzip(url, extract_to="."):
    http_response = urlopen(url)
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path=extract_to)


def asset_to_project(project_id, asset_id, asset_type):
    if asset_id is None:
        print(f"Unable to create member of {asset_type}")
        return
    else:
        asset_id = int(asset_id)  # Note: Is this necessary?

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


def add_provenance(left, right, relation_type, user_id, concept=None):
    payload = json.dumps(
        {
            "left": left.get("id"),
            "left_type": left.get("resource_type"),
            "right": right.get("id"),
            "right_type": right.get("resource_type"),
            "relation_type": relation_type,
            "user_id": user_id,
            "concept": concept,
        }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request(
        "POST",
        url + f"provenance",
        headers=headers,
        data=payload,
    )


resource_provenance_mapping = {
    "datasets": "Dataset",
    "models": "Model",
    "plans": "Plan",
    "intermediates": "Intermediate",
    "publications": "Publication",
    "simulation_runs": "SimulationRun",
    "simulation_parameters": "PlanParameter",
    "model_parameters": "ModelParameter",
}


def add_concept(concept, object_id, type, user_id=1):
    if object_id is None:
        print("No object id is attached to the given concept")
        return
    payload = json.dumps(
        {
            "curie": str(concept),
            "type": str(type),
            "object_id": int(object_id),
            "status": "obj",
        }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request(
        "POST",
        url + f"concepts",
        headers=headers,
        data=payload,
    )
    if type in resource_provenance_mapping:
        # add concept node to neo4j and connect this object to it
        add_provenance(
            left={"id": user_id, "resource_type": "Concept"},
            right={"id": object_id, "resource_type": resource_provenance_mapping[type]},
            relation_type="IS_CONCEPT_OF",
            user_id=user_id,
            concept=concept,
        )


def get_model_concepts(folder, file="/model_mmt_templates.json"):
    model_concepts = []
    with open(folder + file, "r") as f:
        mmt_template = json.load(f)

    for template in mmt_template.get("templates"):

        for key in template.keys():
            if key == "subject" or key == "outcome":

                for identifier in template[key].get("identifiers"):
                    if "biomodels" in identifier:
                        pass
                    else:
                        model_concepts.append(
                            f"{identifier}:{template[key].get('identifiers').get(identifier)}"
                        )
            elif key == "controllers":
                for controller in template[key]:

                    for identifier in controller.get("identifiers"):
                        if "biomodels" in identifier:
                            pass
                        else:
                            model_concepts.append(
                                f"{identifier}:{controller.get('identifiers').get(identifier)}"
                            )
                    for identifier in controller.get("context"):
                        model_concepts.append(
                            f"{identifier}:{controller.get('identifiers').get(identifier)}"
                        )

    return [*set(model_concepts)]
