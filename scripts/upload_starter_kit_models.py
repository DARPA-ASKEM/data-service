import glob
import json
import os
import shutil
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

print("Starting process to upload starter-kit artifacts to postgres.")


def upload_starter_kit_models(person_id=1, project_id=1):
    # loop over models
    folders = glob.glob("experiments*/thin-thread-examples/starter-kit/*/")

    for folder in sorted(folders)[2:3]:

        ## get concepts ##

        model_concepts = get_model_concepts(folder)

        # publications ##

        publication_id = create_publication(path=folder + "document_xdd_gddid.txt")

        asset_to_project(
            project_id=project_id,
            asset_id=publication_id,
            asset_type="publications",
        )

        for concept in model_concepts:
            add_concept(concept=concept, object_id=publication_id, type="publications")
        add_provenance(
            left={"id": project_id, "resource_type": "Project"},
            right={"id": publication_id, "resource_type": "Publication"},
            relation_type="CONTAINS",
            user_id=person_id,
        )

        ## intermediates ##

        intermediate_mmt_id = create_intermediate(
            path=folder + "model_mmt_templates.json",
            type="bilayer",
            source="mrepresentationa",
        )

        asset_to_project(
            project_id=project_id,
            asset_id=intermediate_mmt_id,
            asset_type="intermediates",
        )

        add_provenance(
            left={"id": project_id, "resource_type": "Project"},
            right={"id": intermediate_mmt_id, "resource_type": "Intermediate"},
            relation_type="CONTAINS",
            user_id=person_id,
        )

        for concept in model_concepts:
            add_concept(
                concept=concept, object_id=intermediate_mmt_id, type="intermediates"
            )
        if publication_id:
            add_provenance(
                left={"id": intermediate_mmt_id, "resource_type": "Intermediate"},
                right={"id": publication_id, "resource_type": "Publication"},
                relation_type="EXTRACTED_FROM",
                user_id=person_id,
            )

        for concept in model_concepts:
            add_concept(
                concept=concept, object_id=intermediate_mmt_id, type="intermediates"
            )
        if publication_id:
            add_provenance(
                left={"id": project_id, "resource_type": "Project"},
                right={"id": intermediate_grom_id, "resource_type": "Intermediate"},
                relation_type="CONTAINS",
                user_id=person_id,
            )
            add_provenance(
                left={"id": intermediate_grom_id, "resource_type": "Intermediate"},
                right={"id": publication_id, "resource_type": "Publication"},
                relation_type="EXTRACTED_FROM",
                user_id=person_id,
            )

        intermediate_grom_id = create_intermediate(
            path=f"{folder}model_fn_gromet.json", type="gromet", source="skema"
        )
        asset_to_project(
            project_id=project_id,
            asset_id=intermediate_grom_id,
            asset_type="intermediates",
        )
        add_provenance(
            left={"id": intermediate_grom_id, "resource_type": "Intermediate"},
            right={"id": publication_id, "resource_type": "Publication"},
            relation_type="EXTRACTED_FROM",
            user_id=person_id,
        )
        for concept in model_concepts:
            add_concept(
                concept=concept,
                object_id=intermediate_grom_id,
                type="intermediates",
            )

        ## model ##

        model_description = folder.split("/")[-2] + ": description"
        model_name = folder.split("/")[-2]
        if os.path.exists(folder + "description.json"):
            with open(folder + "description.json", "r") as f:
                desc = f.read()
                model_description = json.loads(desc).get("description", "")

        model_id = create_model(
            path=f"{folder}model_petri.json",
            framework="Petri Net",
            description=model_description,
            name=model_name,
        )

        asset_to_project(project_id=1, asset_id=model_id, asset_type="models")
        add_provenance(
            left={"id": project_id, "resource_type": "Project"},
            right={"id": model_id, "resource_type": "Model"},
            relation_type="CONTAINS",
            user_id=person_id,
        )
        response = requests.request("GET", url + f"models/{model_id}")
        state_model_json = response.json()
        state_id = state_model_json.get("state_id")

        add_provenance(
            left={"id": state_id, "resource_type": "ModelRevision"},
            right={"id": intermediate_grom_id, "resource_type": "Intermediate"},
            relation_type="REINTERPRETS",
            user_id=person_id,
        )
        for concept in model_concepts:
            add_concept(concept=concept, object_id=model_id, type="models")

        ### upload model parameters ###
        print("Model Parameters")
        # load parameters of the model and set the type values
        create_model_parameters(
            path_parameters=f"{folder}model_mmt_parameters.json",
            path_initials=f"{folder}model_mmt_initials.json",
            model_id=model_id,
        )

        ## set concept to inital model parameters

        # get parameters
        response = requests.request("GET", url + f"models/{model_id}/parameters")
        parameters_model_json = response.json()

        with open(f"{folder}model_mmt_initials.json", "r") as f:
            init_params = json.load(f)
            for init_parameter_name, init_parameter_value in init_params.get(
                "initials"
            ).items():
                for parameter in parameters_model_json:
                    if parameter.get("name") == init_parameter_name:
                        ncit = init_parameter_value.get("identifiers").get("ncit", None)
                        ido = init_parameter_value.get("identifiers").get("ido", None)
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

        ### upload simulation plan ###

        simulation_plan_id = create_plan(
            path="scripts/simulation-plan_ATE.json",
            name=f"{model_id}_simulation_plan",
            model_id=model_id,
            description=f"Simulation plan for model {model_id}",
        )

        asset_to_project(project_id=1, asset_id=simulation_plan_id, asset_type="plans")

        add_provenance(
            left={"id": simulation_plan_id, "resource_type": "Plan"},
            relation_type="USES",
            right={"id": state_id, "resource_type": "ModelRevision"},
            user_id=person_id,
        )

        ## create dataset from simulation run * backwards from how this would normally happen but we want dataset id to add to request

        ### simulation run ###

        runs = sorted(glob.glob(folder + "runs/*/"))

        for run in runs:

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
                    add_concept(concept=concept, object_id=dataset_id, type="datasets")

            simulation_run_id = create_run(
                path=run + "output.json",
                plan_id=simulation_plan_id,
                success=True,
                dataset_id=dataset_id,
                description=model_description,
            )

            asset_to_project(
                project_id=1,
                asset_id=simulation_run_id,
                asset_type="simulation_runs",
            )
            add_provenance(
                left={"id": project_id, "resource_type": "Project"},
                right={"id": simulation_plan_id, "resource_type": "Plan"},
                relation_type="CONTAINS",
                user_id=person_id,
            )

            add_provenance(
                left={"id": simulation_run_id, "resource_type": "SimulationRun"},
                relation_type="GENERATED_BY",
                right={"id": simulation_plan_id, "resource_type": "Plan"},
                user_id=person_id,
            )
            add_provenance(
                right={"id": simulation_run_id, "resource_type": "SimulationRun"},
                relation_type="REINTERPRETS",
                left={"id": dataset_id, "resource_type": "Dataset"},
                user_id=person_id,
            )
            add_provenance(
                left={"id": project_id, "resource_type": "Project"},
                right={"id": simulation_run_id, "resource_type": "SimulationRun"},
                relation_type="CONTAINS",
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
                "GET", url + f"simulations/runs/{simulation_run_id}/parameters"
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
                                context = init_parameter_value.get("context", {}).get(
                                    "property", None
                                )
                                if context is not None:
                                    print(f"adding concept context {context}")
                                    add_concept(
                                        concept=context,
                                        object_id=parameter.get("id"),
                                        type="simulation_parameters",
                                    )
                            except Exception as e:
                                print(e)
