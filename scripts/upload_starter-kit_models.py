import glob
import json
import random
import shutil
import time
import xml.etree.ElementTree as ET
from urllib.request import urlopen

import requests
from create_functions import (
    create_framework,
    create_intermediate,
    create_model,
    create_model_parameters,
    create_person,
    create_plan,
    create_project,
    create_publication,
    create_run,
    create_simulation_parameters,
)
from demo_dataset_generator import (
    create_dataset,
    create_feature,
    create_qualifier,
    upload_file_to_tds,
)

# from demo_dataset_generator import programatically_populate_datasets
from json_to_csv import convert_biomd_json_to_csv
from util import (
    add_concept,
    add_provenance,
    asset_to_project,
    download_and_unzip,
    get_model_concepts,
    url,
)

print("Starting process to upload starter-kit artifacts to postgres.")


def upload_starter_kit_models(person_id=1, project_id=1):
    # loop over models
    folders = glob.glob("experiments*/thin-thread-examples/starter-kit/*")
    print(folders)

    with open("scripts/xdd_mapping.json", "r") as f:
        xdd_mapping = json.load(f)

    for folder in folders:
        print(folder)

        ## get concepts ##

        model_concepts = get_model_concepts(folder)
        print(model_concepts)

        # publications ##
        try:

            publication_id = create_publication(path=folder + "document_xdd_gddid.txt")

            asset_to_project(
                project_id=project_id,
                asset_id=int(publication_id),
                asset_type="publications",
            )

            for concept in model_concepts:
                add_concept(
                    concept=concept, object_id=publication_id, type="publications"
                )

        except Exception as e:
            print(e)

        ## intermediates ##
        try:
            intermediate_mmt_id = create_intermediate(
                path=folder + "model_mmt_templates.json",
                type="bilayer",
                source="mrepresentationa",
            )

            asset_to_project(
                project_id=project_id,
                asset_id=int(intermediate_mmt_id),
                asset_type="intermediates",
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
            intermediate_grom_id = create_intermediate(
                path=f"{folder}model_fn_gromet.json", type="gromet", source="skema"
            )
            asset_to_project(
                project_id=project_id,
                asset_id=int(intermediate_grom_id),
                asset_type="intermediates",
            )
            add_provenance(
                left={"id": intermediate_grom_id, "resource_type": "intermediates"},
                right={"id": publication_id, "resource_type": "publications"},
                relation_type="derivedfrom",
                user_id=person_id,
            )
            for concept in model_concepts:
                add_concept(
                    concept=concept,
                    object_id=intermediate_grom_id,
                    type="intermediates",
                )
        except Exception as e:
            print(e)

        ## model ##
        try:

            model_description = folder.split("/")[-1] + ": description"
            model_name = folder.split("/")[-1]

            model_id = create_model(
                path=f"{folder}model_petri.json",
                framework="Petri Net",
                description=model_description,
                name=model_name,
            )

            asset_to_project(project_id=1, asset_id=int(model_id), asset_type="models")

            add_provenance(
                left={"id": model_id, "resource_type": "models"},
                right={"id": intermediate_grom_id, "resource_type": "intermediates"},
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
            response = requests.request("GET", url + f"models/parameters/{model_id}")
            parameters_model_json = response.json()

            with open(f"{folder}model_mmt_initials.json", "r") as f:
                init_params = json.load(f)
                for init_parameter_name, init_parameter_value in init_params.get(
                    "initials"
                ).items():
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
        ### upload simulation plan ###
        try:
            simulation_plan_id = create_plan(
                path="scripts/simulation-plan_ATE.json",
                name=f"{model_id}_simulation_plan",
                model_id=model_id,
                description=f"Simulation plan for model {model_id}",
            )

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

        ### simulation run ###

        try:
            print("Upload Simulation Run")

            simulation_run_id = create_run(
                path=folder + "sim_output.json",
                plan_id=simulation_plan_id,
                success=True,
                dataset_id=None,
            )
            asset_to_project(
                project_id=1,
                asset_id=int(simulation_run_id),
                asset_type="simulation_runs",
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

            create_simulation_parameters(
                path_parameters=f"{folder}model_mmt_parameters.json",
                path_initials=f"{folder}model_mmt_initials.json",
                run_id=simulation_run_id,
            )

            time.sleep(1)
            # get parameters
            response = requests.request(
                "GET", url + f"simulations/runs/parameters/{simulation_run_id}"
            )
            parameters_json = response.json()

            with open(f"{folder}model_mmt_initials.json", "r") as f:
                init_parameters = json.load(f)
                for init_parameter_name, init_parameter_value in init_parameters.get(
                    "initials"
                ).items():
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
        except Exception as e:
            print(e)