import glob
import json
import time
import xml.etree.ElementTree as ET
from urllib.request import urlopen

import requests
import sim_runs_dataset_generator
from create_functions import (
    copy_model,
    create_intermediate,
    create_model_parameters,
    create_plan,
    create_publication,
    create_run,
    create_simulation_parameters,
    update_model,
)

# from demo_dataset_generator import programatically_populate_datasets
from json_to_csv import convert_biomd_json_to_csv
from sim_runs_json_to_csv import convert_sim_runs_to_csv
from util import add_concept, add_provenance, asset_to_project, get_model_concepts, url

print("Upload fake data")

# This array allows you to create abitrary provenance.
# Each dict is a loop which will have access to every type of artifact.
# By setting the artifact_to_id is the id that the new artifact will connect to.
# you can also connect existing artifacts (only publications for now) by setting existing_pub_right and exisiting_pub_left
# The goal is to create a more complicated and interconnected graph to test out search queries.

recipe = [
    {
        "publication_reliationship": "CITES",
        "publication_id_to": 1,
        "existing_pub_left": 2,
        "existing_pub_right": 1,
        "model_name": "Edited model 1. V2",
        "model_relationship": "EDITED_FROM",
        "model_id_to": 2,
        "simulation_relationship": "USES",
        "simulation_id_to": 5,
        "runs_relationship": "GENERATED_BY",
    },
    {
        "model_name": "Edited model 1. V2",
        "model_relationship": "EDITED_FROM",
        "model_id_to": 2,
    },
    {
        "model_name": "Edited model 1. V5",
        "model_relationship": "EDITED_FROM",
        "model_id_to": 2,
        "simulation_relationship": "USES",
        "simulation_id_to": 6,
        "runs_relationship": "GENERATED_BY",
    },
    {
        "model_name": "Model 5",
        "model_relationship": "COPIED_FROM",
        "model_id_to": 1,
    },
    {
        "model_name": "Model 5 v2",
        "model_relationship": "EDITED_FROM",
        "model_id_to": 4,
    },
    {
        "model_name": "Model 7",
        "model_relationship": "COPIED_FROM",
        "model_id_to": 4,
    },
    {
        "dataset_name": "Extracted dataset",
        "dataset_relationship": "EXTRACTED_FROM",
        "publication_id_to": 1,
    },
    {
        "model_name": "Model ?",
        "model_relationship": "COPIED_FROM",
        "model_id_to": 2,
    },
    {
        "model_name": "Model ? v3",
        "model_relationship": "EDITED_FROM",
        "model_id_to": 6,
    },
    {
        "model_name": "Model ? v4",
        "model_relationship": "EDITED_FROM",
        "model_id_to": 6,
    },
    {
        "model_name": "Model ? v5",
        "model_relationship": "COPIED_FROM",
        "model_id_to": 6,
    },
    {
        "publication_reliationship": "CITES",
        "publication_id_to": 1,
    },
]


def upload_fake_provanence_data(person_id=1, project_id=1):
    folders = glob.glob("experiments*/thin-thread-examples/starter-kit/*/")
    prev_model_id = None

    for folder in folders[2:3]:
        model_concepts = get_model_concepts(folder)

        for loop in recipe:

            # add new publicaiton
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
                    left={"id": publication_id, "resource_type": "publication"},
                    right={
                        "id": loop.get("publication_id_to"),
                        "resource_type": "publication",
                    },
                    relation_type=loop.get("publication_reliationship"),
                    user_id=None,
                )

            except Exception as e:
                print(f"failed to upload publication: {e}")

            ##  connect exisiting  publications
            try:

                if loop.get("existing_pub_left", None) is not None:
                    add_provenance(
                        left={
                            "id": loop.get("existing_pub_left"),
                            "resource_type": "publication",
                        },
                        right={
                            "id": loop.get("existing_pub_right"),
                            "resource_type": "publication",
                        },
                        relation_type="CITES",
                        user_id=person_id,
                    )
            except Exception as e:
                print(e)

            ## add new model ##
            try:
                if loop.get("model_name") is None:
                    raise
                model_description = (
                    f"{loop.get('model_relationship')} - {loop.get('model_id_to')} "
                )
                model_name = loop.get("model_name")

                if loop.get("model_relationship") == "EDITED_FROM":
                    update_model(
                        path=f"{folder}model_petri.json",
                        framework="Petri Net",
                        description=model_description,
                        model_id=loop.get("model_id_to"),
                        name=model_name,
                    )
                elif loop.get("model_relationship") == "COPIED_FROM":
                    copy_model(
                        model_id=loop.get("model_id_to"),
                        name=loop.get("model_name"),
                        description=model_description,
                    )

                response = requests.request(
                    "GET", url + f"models/{loop.get('model_id_to')}"
                )
                state_model_json = response.json()
                state_id = state_model_json.get("state_id")

                if loop.get("model_id_to") is None:
                    loop["model_id_to"] = prev_model_id

            except Exception as e:
                print(f" {e}")

            ### upload simulation plan ###
            try:
                if loop.get("simulation_relationship", None) is None:
                    raise
                if loop.get("simulation_id_to", None) is None:
                    loop["simulation_id_to"] = prev_model_id

                simulation_plan_id = create_plan(
                    path="scripts/simulation-plan_ATE.json",
                    name=f"{loop['simulation_id_to']}_simulation_plan",
                    model_id=loop["model_id_to"],
                    description=f"Simulation plan for model {loop['simulation_id_to']}",
                )

                asset_to_project(
                    project_id=1, asset_id=int(simulation_plan_id), asset_type="plans"
                )

                add_provenance(
                    left={"id": simulation_plan_id, "resource_type": "plan"},
                    relation_type=loop.get("simulation_relationship"),
                    right={
                        "id": loop["simulation_id_to"],
                        "resource_type": "model_revision",
                    },
                    user_id=person_id,
                )

            except Exception as e:
                print(f" {e}")

            ### simulation run ###

            try:
                print("starting runs")
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
                    print(
                        f"simulation run id {simulation_plan_id} , {simulation_run_id}"
                    )

                    asset_to_project(
                        project_id=1,
                        asset_id=int(simulation_run_id),
                        asset_type="simulation_runs",
                    )

                    add_provenance(
                        left={
                            "id": simulation_run_id,
                            "resource_type": "simulation_run",
                        },
                        relation_type="GENERATED_BY",
                        right={"id": simulation_plan_id, "resource_type": "plan"},
                        user_id=person_id,
                    )
                    add_provenance(
                        left={
                            "id": simulation_run_id,
                            "resource_type": "simulation_run",
                        },
                        relation_type="REINTERPRETS",
                        right={"id": dataset_id, "resource_type": "dataset"},
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
    # dataset extracted by
    try:
        if loop.get("dataset_relationship", None) is None:
            raise
        runs = glob.glob(folder + "runs/*/")
        for run in runs[1:2]:
            with open(run + "output.json", "r") as f:
                sim_output = f.read()
                sim_output = json.loads(sim_output)

                dataset_response = sim_runs_dataset_generator.create_dataset(
                    maintainer_id=1,
                    dataset_object=sim_output,
                    biomodel_name="Dataset",
                    biomodel_description="Dataset description",
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

                add_provenance(
                    right={
                        "id": loop.get("publication_id_to"),
                        "resource_type": "publication",
                    },
                    relation_type=loop.get("dataset_relationship"),
                    left={"id": dataset_id, "resource_type": "dataset"},
                    user_id=person_id,
                )

    except Exception as e:
        print(e)


# upload_fake_provanence_data()
