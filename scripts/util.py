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


def add_provenance(left, right, relation_type, user_id):
    payload = json.dumps(
        {
            "left": left.get("id"),
            "left_type": left.get("resource_type"),
            "right": right.get("id"),
            "right_type": right.get("resource_type"),
            "relation_type": relation_type,
            "user_id": user_id,
        }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request(
        "POST",
        url + f"provenance",
        headers=headers,
        data=payload,
    )


def add_concept(concept, object_id, type):

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


def get_model_concepts(folder):
    model_concepts = []
    with open(folder + "/model_mmt_templates.json", "r") as f:
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
