import glob
import json
import time
import xml.etree.ElementTree as ET
from urllib.request import urlopen

import requests
import sim_runs_dataset_generator
from create_functions import (
    create_intermediate,
    create_model,
    create_model_parameters,
    create_plan,
    create_publication,
    create_run,
    create_simulation_parameters,
)

# from demo_dataset_generator import programatically_populate_datasets
from json_to_csv import convert_biomd_json_to_csv
from sim_runs_json_to_csv import convert_sim_runs_to_csv
from util import add_concept, add_provenance, asset_to_project, get_model_concepts, url

print("Upload fake data")


recipe = [
    {
        "publication_reliationship": "CITES",
        "publication_id_to": 1,
        "model_name": "Edited model 1. V2",
        "model_relationship": "EDITED_FROM",
        "model_id_to": 1,
    },
    {
        "publication_reliationship": "CITES",
        "publication_id_to": 1,
        "model_name": "Edited model 1. V3",
        "model_relationship": "EDITED_FROM",
        "model_id_to": 4,
    },
    {
        "publication_reliationship": "CITES",
        "publication_id_to": 3,
        "model_name": "Merged",
    },
]


def upload_fake_provanence_data(person_id=1, project_id=1):
    print("start")
    # loop over models
    folders = glob.glob("experiments*/thin-thread-examples/starter-kit/*/")
    prev_model_id = None
    print(folders)
    for folder in folders[2:3]:
        print(folder)
        model_concepts = get_model_concepts(folder)

        for loop in recipe:
            print(loop)
            # publications ##
            try:
                if loop.get("publication_reliationship", None) is None:
                    raise

                publication_id = create_publication(
                    path=folder + "document_xdd_gddid.txt"
                )
                print(publication_id)

                asset_to_project(
                    project_id=project_id,
                    asset_id=int(publication_id),
                    asset_type="publications",
                )

                for concept in model_concepts:
                    add_concept(
                        concept=concept, object_id=publication_id, type="publications"
                    )
                add_provenance(
                    left={"id": publication_id, "resource_type": "publications"},
                    right={
                        "id": loop.get("publication_id_to"),
                        "resource_type": "publications",
                    },
                    relation_type=loop.get("publication_reliationship"),
                    user_id=person_id,
                )

            except Exception as e:
                print(f"failed to upload publication: {e}")

            ## model ##
            try:
                if loop.get("model_name") is None:
                    raise
                model_description = (
                    f"{loop.get('model_relationship')} - {loop.get('model_id_to')} "
                )
                model_name = loop.get("model_name")

                model_id = create_model(
                    path=f"{folder}model_petri.json",
                    framework="Petri Net",
                    description=model_description,
                    name=model_name,
                )
                prev_model_id = model_id

                asset_to_project(
                    project_id=1, asset_id=int(model_id), asset_type="models"
                )

                ### upload model parameters ###
                try:
                    print("Model Parameters")
                    # load parameters of the model and set the type values
                    create_model_parameters(
                        path_parameters=f"{folder}model_mmt_parameters.json",
                        path_initials=f"{folder}model_mmt_initials.json",
                        model_id=model_id,
                    )

                except Exception as e:
                    print(e)

                ## set concept to inital model parameters
                try:
                    # get parameters
                    response = requests.request(
                        "GET", url + f"models/parameters/{model_id}"
                    )
                    parameters_model_json = response.json()

                    with open(f"{folder}model_mmt_initials.json", "r") as f:
                        init_params = json.load(f)
                        for (
                            init_parameter_name,
                            init_parameter_value,
                        ) in init_params.get("initials").items():
                            for parameter in parameters_model_json:
                                if parameter.get("name") == init_parameter_name:
                                    ncit = init_parameter_value.get("identifiers").get(
                                        "ncit", None
                                    )
                                    ido = init_parameter_value.get("identifiers").get(
                                        "ido", None
                                    )
                                    if ncit is not None:
                                        add_concept(
                                            concept=f"ncit:{ncit}",
                                            object_id=parameter.get("id"),
                                            type="model_parameters",
                                        )
                                    if ido is not None:
                                        add_concept(
                                            concept=f"ido:{ido}",
                                            object_id=parameter.get("id"),
                                            type="model_parameters",
                                        )
                except Exception as e:
                    print(e)
                if loop.get("model_id_to") is None:
                    loop["model_id_to"] = prev_model_id

                add_provenance(
                    left={"id": model_id, "resource_type": "models"},
                    right={"id": loop.get("model_id_to"), "resource_type": "models"},
                    relation_type=loop.get("model_relationship"),
                    user_id=person_id,
                )
                for concept in model_concepts:
                    add_concept(concept=concept, object_id=model_id, type="models")

            except Exception as e:
                print(f" {e}")

            except Exception as e:
                print(e)
            ### upload simulation plan ###
            try:
                if loop.get("simulation_relationship", None) is None:
                    raise
                if loop.get("simulation_id_to", None) is None:
                    loop["simulation_id_to"] = prev_model_id
                simulation_plan_id = create_plan(
                    path="scripts/simulation-plan_ATE.json",
                    name=f"{loop['simulation_id_to']}_simulation_plan",
                    model_id=loop["simulation_id_to"],
                    description=f"Simulation plan for model {loop['simulation_id_to']}",
                )

                asset_to_project(
                    project_id=1, asset_id=int(simulation_plan_id), asset_type="plans"
                )

                add_provenance(
                    left={"id": simulation_plan_id, "resource_type": "plans"},
                    relation_type="USES",
                    right={"id": loop["simulation_id_to"], "resource_type": "models"},
                    user_id=person_id,
                )

            except Exception as e:
                print(f" {e}")

            ## create dataset from simulation run * backwards from how this would normally happen but we want dataset id to add to request

            ### simulation run ###

            try:
                runs = glob.glob(folder + "runs/*/")
                if loop.get("runs_relationship", None) is None:
                    raise
                for run in runs[1:4]:

                    # load simulation run contents as json
                    with open(run + "output.json", "r") as f:
                        sim_output = f.read()
                        sim_output = json.loads(sim_output)

                        # Create the dataset with maintainer_id of 1
                        # assuming the first maintainer is already created.
                        model_description = (
                            run.split("/")[-4]
                            + " was used to create this dataset. Run number "
                            + run.split("/")[-2]
                        )
                        model_name = (
                            "Simulation output from "
                            + run.split("/")[-4]
                            + " : run number "
                            + run.split("/")[-2]
                        )

                        dataset_response = sim_runs_dataset_generator.create_dataset(
                            maintainer_id=1,
                            dataset_object=sim_output,
                            biomodel_name=model_name,
                            biomodel_description=model_description,
                            url=url,
                        )
                        dataset_id = dataset_response["id"]
                        # Convert the json to a CSV
                        convert_sim_runs_to_csv(
                            json_file_path=run + "output.json",
                            output_file_path=run + "sim_output.csv",
                        )
                        # Upload the CSV to TDS for full mock data
                        with open(run + "sim_output.csv", "rb") as sim_csv:
                            print(f"Uploading file to dataset_id {dataset_id}")
                            sim_runs_dataset_generator.upload_file_to_tds(
                                id=dataset_id, file_object=sim_csv, url=url
                            )
                        # Finish populating dataset metadata: Features, Qualifiers
                        for feature_obj in list(sim_output.values()):
                            sim_runs_dataset_generator.create_feature(
                                dataset_id, feature_obj, url=url
                            )
                        sim_runs_dataset_generator.create_qualifier(
                            dataset_id, sim_output, url=url
                        )
                        asset_to_project(project_id, dataset_id, "datasets")
                        for concept in model_concepts:
                            add_concept(
                                concept=concept, object_id=dataset_id, type="datasets"
                            )

                    simulation_run_id = create_run(
                        path=run + "output.json",
                        plan_id=simulation_plan_id,
                        success=True,
                        dataset_id=dataset_id,
                        description=model_description,
                    )

                    asset_to_project(
                        project_id=1,
                        asset_id=int(simulation_run_id),
                        asset_type="simulation_runs",
                    )

                    add_provenance(
                        left={
                            "id": simulation_run_id,
                            "resource_type": "simulation_runs",
                        },
                        relation_type="DERIVED_FROM",
                        right={"id": simulation_plan_id, "resource_type": "plans"},
                        user_id=person_id,
                    )
                    add_provenance(
                        left={
                            "id": simulation_run_id,
                            "resource_type": "simulation_runs",
                        },
                        relation_type="GENERATED_BY",
                        right={"id": dataset_id, "resource_type": "datasets"},
                        user_id=person_id,
                    )

                    ## add simulation parameters ##
                    create_simulation_parameters(
                        path_parameters=f"{run}parameters.json",
                        path_initials=f"{run}initials.json",
                        run_id=simulation_run_id,
                    )

                    time.sleep(1)
                    # get parameters
                    response = requests.request(
                        "GET", url + f"simulations/runs/parameters/{simulation_run_id}"
                    )
                    parameters_json = response.json()

                    with open(f"{run}initials.json", "r") as f:
                        init_parameters = json.load(f)
                        for (
                            init_parameter_name,
                            init_parameter_value,
                        ) in init_parameters.get("initials").items():
                            for parameter in parameters_json:
                                if parameter.get("name") == init_parameter_name:
                                    ncit = init_parameter_value.get("identifiers").get(
                                        "ncit", None
                                    )
                                    ido = init_parameter_value.get("identifiers").get(
                                        "ido", None
                                    )
                                    if ncit is not None:
                                        add_concept(
                                            concept=f"ncit:{ncit}",
                                            object_id=parameter.get("id"),
                                            type="simulation_parameters",
                                        )
                                    if ido is not None:
                                        add_concept(
                                            concept=f"ido:{ido}",
                                            object_id=parameter.get("id"),
                                            type="simulation_parameters",
                                        )
                                    ## add context concept as well ##
                                    try:
                                        context = init_parameter_value.get(
                                            "context", {}
                                        ).get("property", None)
                                        if context is not None:
                                            print(f"adding concept context {context}")
                                            add_concept(
                                                concept=context,
                                                object_id=parameter.get("id"),
                                                type="simulation_parameters",
                                            )
                                    except Exception as e:
                                        print(e)
            except Exception as e:
                print(e)


# upload_fake_provanence_data()
