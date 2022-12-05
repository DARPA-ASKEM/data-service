import glob
import json
import random
import shutil
import time
import xml.etree.ElementTree as ET
from urllib.request import urlopen

import requests
import sim_runs_dataset_generator

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
from exemplar_dataset_generator import populate_exemplar_datasets
from json_to_csv import convert_biomd_json_to_csv
from sim_runs_json_to_csv import convert_sim_runs_to_csv

from util import (
    add_concept,
    add_provenance,
    asset_to_project,
    download_and_unzip,
    get_model_concepts,
    url,
)

print("Starting process to upload artifacts to postgres.")


# download_and_unzip(
#     "https://github.com/DARPA-ASKEM/experiments/archive/refs/heads/main.zip"
# )
time.sleep(2)

person = create_person()
person_id = person.get("id")
project = create_project()
project_id = project.get("id")
create_framework()

# loop over models
folders = glob.glob("experiments*/thin-thread-examples/biomodels/BIOMD*/")


for folder in folders[1:2]:
    # get src/main files
    folders_src = glob.glob(folder + "src/main/*")

    ## get concepts ##

    model_concepts = get_model_concepts(folder)
    print(model_concepts)

    # publications ##
    try:

        publication_id = create_publication(path=folder + "document_xdd_gddid.txt")

        asset_to_project(
            project_id=1, asset_id=int(publication_id), asset_type="publications"
        )

        for concept in model_concepts:
            add_concept(concept=concept, object_id=publication_id, type="publications")

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
        intermediate_sbml_id = create_intermediate(
            path=folders_src[0], type="sbml", source="mrepresentationa"
        )
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
        tree = ET.parse(folders_src[0])
        root = tree.getroot()
        model_description = root[0][0][0][0].text
        model_name = root[0].attrib["name"]

        model_id = create_model(
            path=f"{folder}model_petri.json",
            framework="Petri Net",
            description=model_description,
            name=model_name,
        )

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
                biomodel_description=model_description,
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
            for concept in model_concepts:
                add_concept(concept=concept, object_id=dataset_id, type="datasets")

    except FileNotFoundError:
        print("sim_output.json not found in " + folder)

    ### simulation run ###

    try:
        print("Upload Simulation Run")

        simulation_run_id = create_run(
            path=folder + "sim_output.json",
            plan_id=simulation_plan_id,
            success=True,
            dataset_id=dataset_id,
        )
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
                        ncit = init_parameter_value.get("identifiers").get("ncit", None)
                        ido = init_parameter_value.get("identifiers").get("ido", None)
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

    ### upload simulation run datasets ####

    try:

        print("Upload Simulation Run Datasets")

        runs = glob.glob(folder + "runs/*/")

        for run in runs:

            # load simulation run contents as json
            with open(run + "output.json", "r") as f:
                sim_output = f.read()
                sim_output = json.loads(sim_output)

                # Create the dataset with maintainer_id of 1
                # assuming the first maintainer is already created.

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

        
            simulation_run_id = create_run(path=run + "output.json", plan_id=simulation_plan_id, success=True, dataset_id=dataset_id)

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

    except FileNotFoundError:
        print("output.json not found in " + run)


populate_exemplar_datasets()

## now delete repo
# shutil.rmtree("experiments-main")
