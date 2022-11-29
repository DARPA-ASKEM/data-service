import glob
import json
import random
import shutil
import time
import xml.etree.ElementTree as ET
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

import requests
from demo_dataset_generator import (
    create_dataset,
    create_feature,
    create_qualifier,
    upload_file_to_tds,
)

# from demo_dataset_generator import programatically_populate_datasets
from exemplar_dataset_generator import populate_exemplar_datasets
from json_to_csv import convert_biomd_json_to_csv

url = "http://localhost:8001/"


def download_and_unzip(url, extract_to="."):
    http_response = urlopen(url)
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path=extract_to)


time.sleep(5)

print("Starting process to upload artifacts to postgres.")


download_and_unzip(
    "https://github.com/DARPA-ASKEM/experiments/archive/refs/heads/main.zip"
)
time.sleep(2)

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


person = create_person()
person_id = person.get("id")
project = create_project()
project_id = project.get("id")
create_framework()

# loop over models
folders = glob.glob("experiments*/thin-thread-examples/biomodels/BIOMD*/")


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


for folder in folders:
    # get src/main files
    folders_src = glob.glob(folder + "src/main/*")

    ## get concepts ##
    model_concepts = []
    with open(folder + "model_mmt_templates.json", "r") as f:
        mmt_template = json.load(f)

    for template in mmt_template.get("templates"):

        for key in template.keys():
            if key == "subject" or key == "outcome":
                ncit = template[key].get("identifiers").get("ncit", None)
                ido = template[key].get("identifiers").get("ido", None)
                if ncit is not None:
                    model_concepts.append(f"ncit:{ncit}")
                if ido is not None:
                    model_concepts.append(f"ido:{ido}")

    model_concepts = [*set(model_concepts)]

    # publications ##
    try:
        print("Upload publication")

        with open(folder + "document_xdd_gddid.txt", "r") as f:
            gddid = f.read()

        payload = json.dumps({"xdd_uri": f"{gddid}"})
        headers = {"Content-Type": "application/json"}

        # return resource_id (a1)
        response = requests.request(
            "POST", url + "external/publications", headers=headers, data=payload
        )
        publication_json = response.json()
        publication_id = publication_json.get("id")
        asset_to_project(
            project_id=1, asset_id=int(publication_id), asset_type="publications"
        )

        for concept in model_concepts:
            add_concept(concept=concept, object_id=publication_id, type="publications")
    except Exception as e:
        print(f"error opening {folder}document_doi.txt . - {e}")

    ## intermediates ##
    try:
        print("Upload intermediate mmt")
        with open(folder + "model_mmt_templates.json", "r") as f:
            mmt_template = json.load(f)

            payload = json.dumps(
                {
                    "source": "mrepresentationa",
                    "type": "bilayer",
                    "content": json.dumps(mmt_template),
                }
            )
        headers = {"Content-Type": "application/json"}

        response = requests.request(
            "POST", url + "models/intermediates", headers=headers, data=payload
        )
        intermediate_json = response.json()
        intermediate_mmt_id = intermediate_json.get("id")

        asset_to_project(
            project_id=1, asset_id=int(intermediate_mmt_id), asset_type="intermediates"
        )

        add_provenance(
            left={"id": intermediate_mmt_id, "resource_type": "intermediates"},
            right={"id": publication_id, "resource_type": "publications"},
            relation_type="derivedfrom",
            user_id=person_id,
        )
        for concept in model_concepts:
            add_concept(
                concept=concept, object_id=intermediate_mmt_id, type="intermediates"
            )

    except Exception as e:
        print(e)

    try:
        print("Upload intermediate sbml")

        with open(folders_src[0], "r") as f:
            mmt_template = f.read()
            payload = json.dumps(
                {
                    "source": "mrepresentationa",
                    "type": "sbml",
                    "content": mmt_template,
                }
            )
        headers = {"Content-Type": "application/json"}

        response = requests.request(
            "POST", url + "models/intermediates", headers=headers, data=payload
        )
        intermediate_json = response.json()
        intermediate_sbml_id = intermediate_json.get("id")
        asset_to_project(
            project_id=1, asset_id=int(intermediate_sbml_id), asset_type="intermediates"
        )
        add_provenance(
            left={"id": intermediate_sbml_id, "resource_type": "intermediates"},
            right={"id": intermediate_mmt_id, "resource_type": "intermediates"},
            relation_type="derivedfrom",
            user_id=person_id,
        )
        for concept in model_concepts:
            add_concept(
                concept=concept, object_id=intermediate_sbml_id, type="intermediates"
            )

    except Exception as e:
        print(e)

    ## model ##
    try:
        print("Upload Model")

        # model content
        with open(f"{folder}model_petri.json", "r") as f:
            model_content = json.load(f)

        tree = ET.parse(folders_src[0])
        root = tree.getroot()
        model_description = root[0][0][0][0].text
        model_name = root[0].attrib["name"]

        payload = json.dumps(
            {
                "name": model_name,
                "description": model_description,
                "content": json.dumps(model_content),
                "framework": "Petri Net",
            }
        )
        headers = {"Content-Type": "application/json"}

        response = requests.request(
            "POST", url + "models", headers=headers, data=payload
        )
        model_json = response.json()
        model_id = model_json.get("id")
        asset_to_project(project_id=1, asset_id=int(model_id), asset_type="models")

        add_provenance(
            left={"id": model_id, "resource_type": "models"},
            right={"id": intermediate_sbml_id, "resource_type": "intermediates"},
            relation_type="derivedfrom",
            user_id=person_id,
        )
        for concept in model_concepts:
            add_concept(concept=concept, object_id=model_id, type="models")

    except Exception as e:
        print(f" {e}")

    ### upload model parameters ###
    try:
        print("Model Parameters")
        # load parameters of the model and set the type values
        parameter_types = []
        with open(f"{folder}model_mmt_parameters.json", "r") as f:
            parameters = json.load(f)
            for parameter_name, parameter_value in parameters.get("parameters").items():
                param = {
                    "model_id": model_id,
                    "name": parameter_name,
                    "type": str(type(parameter_value.get("value")).__name__),
                    "default_value": str(parameter_value.get("value")),
                    "initial": False,
                }
                parameter_types.append(param)

        with open(f"{folder}model_mmt_initials.json", "r") as f:
            parameters = json.load(f)
            for parameter_name, parameter_value in parameters.get("initials").items():
                param = {
                    "model_id": model_id,
                    "name": parameter_name,
                    "type": str(type(parameter_value.get("value")).__name__),
                    "default_value": str(parameter_value.get("value")),
                    "initial": True,
                }
                parameter_types.append(param)

        payload = json.dumps(parameter_types)
        headers = {"Content-Type": "application/json"}
        response = requests.request(
            "PUT", url + f"models/parameters/{model_id}", headers=headers, data=payload
        )

    except Exception as e:
        print(e)
    ### upload simulation plan ###
    try:
        print("Upload Simulation Plan")

        path = "simulations/plans"

        # load simulation plan contents as json
        with open("scripts/simulation-plan_ATE.json", "r") as f:
            simulation_body = json.load(f)

        payload = json.dumps(
            {
                "name": f"{model_id}_simulation_plan",
                "model_id": model_id,
                "description": f"Simulation plan for model {model_id}",
                "simulator": "default",
                "query": "My query",
                "content": json.dumps(simulation_body),
                # "parameters":json.dumps({"simulations":{"count":5}})
            }
        )
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url + path, headers=headers, data=payload)
        sim_plan_json = response.json()
        simulation_plan_id = sim_plan_json.get("id")

        asset_to_project(
            project_id=1, asset_id=int(simulation_plan_id), asset_type="plans"
        )

        add_provenance(
            left={"id": simulation_plan_id, "resource_type": "plans"},
            relation_type="derivedfrom",
            right={"id": model_id, "resource_type": "models"},
            user_id=person_id,
        )

    except Exception as e:
        print(f" {e}")

    ## create dataset from simulation run * backwards from how this would normally happen but we want dataset id to add to request

    try:
        # Open json to get relevant information
        with open(folder + "sim_output.json", "r", encoding="utf-8") as sim_out:
            # model_name = folder.split("/")[-2]
            simulation_output = json.load(sim_out)
            states = simulation_output["states"]
            first_state_obj = states[0]
            num_of_states = len(first_state_obj)

            # Create the dataset with maintainer_id of 1
            # assuming the first maintainer is already created.
            dataset_response = create_dataset(
                maintainer_id=1,
                num_of_states=num_of_states,
                biomodel_name=model_name,
                url=url,
            )
            dataset_id = dataset_response["id"]
            # Convert the json to a CSV
            convert_biomd_json_to_csv(
                json_file_path=folder + "sim_output.json",
                output_file_path=folder + "sim_output.csv",
            )
            # Upload the CSV to TDS for full mock data
            with open(folder + "sim_output.csv", "rb") as sim_csv:
                print(f"Uploading file to dataset_id {dataset_id}")
                upload_file_to_tds(id=dataset_id, file_object=sim_csv, url=url)
            # Finish populating dataset metadata: Features, Qualifiers
            for state in range(num_of_states):
                create_feature(dataset_id, state, url=url)
            create_qualifier(dataset_id, num_of_states, url=url)
            asset_to_project(project_id, dataset_id, "datasets")

    except FileNotFoundError:
        print("sim_output.json not found in " + folder)

    ### simulation run ###

    try:
        print("Upload Simulation Run")

        path = "simulations/runs/descriptions"

        # load simulation run contents as json
        with open(folder + "sim_output.json", "r") as f:
            sim_output = f.read()

        payload = json.dumps(
            {
                "simulator_id": simulation_plan_id,
                "success": True,
                "response": json.dumps(sim_output),
                "dataset_id": dataset_id,
            }
        )
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url + path, headers=headers, data=payload)
        sim_run_json = response.json()
        simulation_run_id = sim_run_json.get("id")

        asset_to_project(
            project_id=1, asset_id=int(simulation_run_id), asset_type="simulation_runs"
        )

        add_provenance(
            left={"id": simulation_run_id, "resource_type": "simulation_runs"},
            relation_type="derivedfrom",
            right={"id": simulation_plan_id, "resource_type": "plans"},
            user_id=person_id,
        )

    except Exception as e:
        print(f" {e}")

    ### Simulation parameters ###
    try:

        # creating simulation parameters
        parameter_simulation = []
        with open(f"{folder}model_mmt_parameters.json", "r") as f:
            parameters = json.load(f)
            for parameter_name, parameter_value in parameters.get("parameters").items():
                parameter_simulation.append(
                    {
                        "name": parameter_name,
                        "value": str(parameter_value.get("value")),
                        "type": str(type(parameter_value.get("value")).__name__),
                    }
                )

        payload = json.dumps(parameter_simulation)
        headers = {"Content-Type": "application/json"}
        response = requests.request(
            "PUT",
            url + f"simulations/runs/parameters/{simulation_run_id}",
            headers=headers,
            data=payload,
        )

        # get parameters
        response = requests.request(
            "GET", url + f"simulations/runs/parameters/{simulation_run_id}"
        )
        parameters_json = response.json()

        # for parameter in parameters_json:

        #     add_concept(
        #         concept=concept,
        #         object_id=parameter.get("id"),
        #         type="simulation_parameters",
        #     )

    except Exception as e:
        print(e)

populate_exemplar_datasets()

## now delete repo
shutil.rmtree("experiments-main")
