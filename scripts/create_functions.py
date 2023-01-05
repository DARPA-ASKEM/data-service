import json
from json.decoder import JSONDecodeError
from typing import Optional

import requests
from util import asset_to_project, url


#### Person ####
def create_person(url=url):
    path = "persons"

    payload = json.dumps(
        {
            "name": "Adam Smith",
            "email": "Adam@test.io",
            "org": "Uncharted",
            "website": "",
            "is_registered": True,
        }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url + path, headers=headers, data=payload)

    return response.json()


#### Project ####


def create_project(url=url):
    path = "projects"

    payload = json.dumps(
        {
            "name": "My Project",
            "description": "First project in TDS",
            "assets": {},
            "status": "active",
        }
    )
    headers = {"Content-Type": "application/json"}

    # return project id (p1)
    response = requests.request("POST", url + path, headers=headers, data=payload)

    return response.json()


#### Framework ####


def create_framework(url=url):
    path = "models/frameworks"

    payload = json.dumps(
        {
            "name": "Petri Net",
            "version": "0.0.1",
            "semantics": "semantics_go_here",
        }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url + path, headers=headers, data=payload)

    return response.text


## create publication ###
def create_publication(path, url=url, title="xdd_mapping") -> Optional[int]:
    print("Upload publication")

    with open(path, "r") as f:
        gddid = f.read()

    if gddid is None or gddid == "":
        print("Missing gddid")
        return None

    with open("scripts/xdd_mapping.json", "r") as f:
        xdd_mapping = json.load(f)

    if title == "xdd_mapping":
        try:
            title = xdd_mapping[gddid]
        except KeyError as e:
            print(
                f"Publication title not found in xdd_mapping. Might need to resync with xdd. Error: {e}. Setting title to Unknown"
            )
            title = "Unknown"

    payload = json.dumps({"xdd_uri": f"{gddid}", "title": title})
    headers = {"Content-Type": "application/json"}

    # return resource_id (a1)
    response = requests.request(
        "POST", url + "external/publications", headers=headers, data=payload
    )
    publication_json = response.json()
    publication_id = publication_json.get("id")
    return publication_id


def create_intermediate(path, type, source, url=url) -> Optional[int]:
    print("Create intermediate")
    with open(path, "r") as f:
        if type == "sbml":
            template = f.read()
            payload = json.dumps(
                {
                    "source": source,
                    "type": type,
                    "content": template,
                }
            )
        else:
            try:
                template = json.load(f)
            except JSONDecodeError:
                print("Failed: Unable to decode intermediate")
                return

            payload = json.dumps(
                {
                    "source": source,
                    "type": type,
                    "content": json.dumps(template),
                }
            )
    headers = {"Content-Type": "application/json"}

    response = requests.request(
        "POST", url + "models/intermediates", headers=headers, data=payload
    )
    intermediate_json = response.json()
    intermediate_id = intermediate_json.get("id")
    return intermediate_id


def create_model(path, name, description, framework, url=url):
    print("Upload Model")

    with open(path, "r") as f:
        model_content = json.load(f)
    payload = json.dumps(
        {
            "name": name,
            "description": description,
            "content": json.dumps(model_content),
            "framework": framework,
        }
    )
    headers = {"Content-Type": "application/json"}
    print(payload)
    response = requests.request("POST", url + "models", headers=headers, data=payload)
    print(response.text)
    model_json = response.json()
    model_id = model_json.get("id")
    return model_id


def update_model(path, name, description, framework, model_id, url=url):
    print("Upload Model")

    with open(path, "r") as f:
        model_content = json.load(f)
    print(model_content)
    payload = json.dumps(
        {
            "name": name,
            "description": description,
            "content": json.dumps(model_content),
            "framework": framework,
        }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request(
        "POST", url + f"models/{model_id}", headers=headers, data=payload
    )
    print(response.text)
    model_json = response.json()
    model_id = model_json.get("id")
    return model_id


def copy_model(model_id, name, description, url=url):
    print("Upload Model")

    payload = json.dumps(
        {"name": name, "description": description, "user_id": 1, "left": model_id}
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request(
        "POST", url + f"models/opts/copy", headers=headers, data=payload
    )
    model_json = response.json()
    model_id = model_json.get("id")
    return model_id


def create_plan(
    path, model_id, name, description, simulator="default", query="A query", url=url
):
    print("Upload Simulation Plan")
    with open(path, "r") as f:
        simulation_body = json.load(f)

    payload = json.dumps(
        {
            "name": name,
            "model_id": model_id,
            "description": description,
            "simulator": simulator,
            "query": query,
            "content": json.dumps(simulation_body),
        }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request(
        "POST", url + "simulations/plans", headers=headers, data=payload
    )
    sim_plan_json = response.json()
    simulation_plan_id = sim_plan_json.get("id")
    return simulation_plan_id


def create_run(path, plan_id, success, description=None, dataset_id=None, url=url):
    # load simulation run contents as json
    with open(path, "r") as f:
        sim_output = f.read()

    payload = json.dumps(
        {
            "simulator_id": plan_id,
            "success": success,
            "response": json.dumps(sim_output),
            "dataset_id": dataset_id,
            "description": description,
        }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request(
        "POST", url + "simulations/runs/descriptions", headers=headers, data=payload
    )
    sim_run_json = response.json()
    simulation_run_id = sim_run_json.get("id")
    return simulation_run_id


def create_model_parameters(path_parameters, path_initials, model_id, url=url):
    print("uploading model parameters")

    parameter_types = []
    with open(path_parameters, "r") as f:
        parameters = json.load(f)
    for parameter_name, parameter_value in parameters.get("parameters").items():
        if parameter_value.get("value") == None:
            type_ = "float"
            default_value = None
        else:
            type_ = str(type(parameter_value.get("value")).__name__)
            default_value = str(parameter_value.get("value"))

        param = {
            "model_id": model_id,
            "name": parameter_name,
            "type": type_,
            "default_value": default_value,
            "state_variable": False,
        }
        parameter_types.append(param)


        payload = json.dumps(parameter_types)
        headers = {"Content-Type": "application/json"}
        response = requests.request(
            "PUT", url + f"models/{model_id}/parameters", headers=headers, data=payload
        )
        return response


def create_simulation_parameters(
    path_parameters, path_initials, run_id, concepts=True, url=url
):
    print("uploading simulation parameters")
    # creating simulation parameters
    parameter_simulation = []
    with open(path_parameters, "r") as f:
        parameters = json.load(f)
        print(parameters)
        for parameter_name, parameter_value in parameters.get("parameters").items():
            parameter_simulation.append(
                {
                    "name": parameter_name,
                    "value": str(parameter_value.get("value")),
                    "type": str(type(parameter_value.get("value")).__name__),
                }
            )
    with open(path_initials, "r") as f:
        parameters = json.load(f)
        for parameter_name, parameter_value in parameters.get("initials").items():
            param = {
                "name": parameter_name,
                "type": str(type(parameter_value.get("value")).__name__),
                "value": str(parameter_value.get("value")),
            }
            parameter_simulation.append(param)

    payload = json.dumps(parameter_simulation)
    headers = {"Content-Type": "application/json"}
    response = requests.request(
        "PUT",
        url + f"simulations/runs/{run_id}/parameters",
        headers=headers,
        data=payload,
    )
    return response
