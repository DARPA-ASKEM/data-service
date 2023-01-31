import argparse
import glob
import json
import os

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
from util import (
    add_concept,
    add_provenance,
    asset_to_project,
    download_and_unzip,
    get_model_concepts,
    url,
)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--url",
    help="Url of tds",
    default="",
)
args = parser.parse_args()
print(args)


folders = sorted(
    glob.glob("experiments*/thin-thread-examples/milestone_6month/evaluation/indra/*")
)

scenario_1 = sorted(glob.glob(folders[0] + "/*"))
scenario_2 = sorted(glob.glob(folders[1] + "/*"))
scenario_3 = sorted(glob.glob(folders[2] + "/*"))
scenario_tuples = []
for scenario in scenario_2:
    scenario_tuples.append(("2", scenario))
for scenario in scenario_3:
    scenario_tuples.append(("3", scenario))

for ind, scenario in scenario_tuples:

    situation = scenario.split("/")[-1]

    model_concepts = get_model_concepts(scenario, file="/model_mmt.json")
    publication_id = create_publication(
        path=scenario + "/document_xdd_gddid.txt", url=args.url
    )

    asset_to_project(
        project_id=1,
        asset_id=int(publication_id),
        asset_type="publications",
        url=args.url,
    )

    # intermediate
    intermediate_mmt_id = create_intermediate(
        path=scenario + "/model_mmt.json",
        type="bilayer",
        source="mrepresentationa",
        url=args.url,
    )

    asset_to_project(
        project_id=1,
        asset_id=int(intermediate_mmt_id),
        asset_type="intermediates",
        url=args.url,
    )
    add_provenance(
        left={"id": intermediate_mmt_id, "resource_type": "Intermediate"},
        right={"id": publication_id, "resource_type": "Publication"},
        relation_type="EXTRACTED_FROM",
        user_id=1,
        url=args.url,
    )
    for concept in model_concepts:
        add_concept(
            concept=concept,
            object_id=intermediate_mmt_id,
            type="intermediates",
            url=args.url,
        )

    model_id = create_model(
        path=f"{scenario}/model_petri.json",
        framework="Petri Net",
        description=f"DARPA-ASKEM Evaluation Scenario {ind}",
        name=situation,
        url=args.url,
    )

    asset_to_project(
        project_id=1, asset_id=int(model_id), asset_type="models", url=args.url
    )

    response = requests.request("GET", args.url + f"models/{model_id}")
    state_model_json = response.json()
    state_id = state_model_json.get("state_id")

    add_provenance(
        left={"id": state_id, "resource_type": "ModelRevision"},
        right={"id": intermediate_mmt_id, "resource_type": "Intermediate"},
        relation_type="REINTERPRETS",
        user_id=1,
        url=args.url,
    )

    for concept in model_concepts:
        add_concept(concept=concept, object_id=model_id, type="models", url=args.url)

    ### upload model parameters ###
    print("Model Parameters")
    # load parameters of the model and set the type values
    create_model_parameters(
        path_parameters=f"{scenario}/model_mmt_parameters.json",
        path_initials=f"{scenario}/model_mmt_initials.json",
        model_id=model_id,
        url=args.url,
    )

    # ## set concept to inital model parameters
    # get parameters
    response = requests.request("GET", args.url + f"models/{model_id}/parameters")
    parameters_model_json = response.json()
    with open(f"{scenario}/model_mmt_initials.json", "r") as f:
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
                            url=args.url,
                        )
                    if ido is not None:
                        add_concept(
                            concept=f"ido:{ido}",
                            object_id=parameter.get("id"),
                            type="model_parameters",
                            url=args.url,
                        )

    # model

for scenario in scenario_1:
    model_concepts = get_model_concepts(scenario + "/", file="/model_mmt.json")
    print(model_concepts)

    situation = scenario.split("/")[-1]

    intermediate_mmt_id = create_intermediate(
        path=scenario + "/model_mmt.json",
        type="bilayer",
        source="mrepresentationa",
        url=args.url,
    )

    asset_to_project(
        project_id=1,
        asset_id=int(intermediate_mmt_id),
        asset_type="intermediates",
        url=args.url,
    )
    ## create model
    if situation == "sir":
        name = "SIR"
    else:
        name = "SIR-" + situation

    model_id = create_model(
        path=f"{scenario}/model_petri.json",
        framework="Petri Net",
        description=f"DARPA-ASKEM Evaluation Scenario 1",
        name=name,
        url=args.url,
    )

    asset_to_project(
        project_id=1, asset_id=int(model_id), asset_type="models", url=args.url
    )

    response = requests.request("GET", args.url + f"models/{model_id}")
    state_model_json = response.json()
    state_id = state_model_json.get("state_id")

    add_provenance(
        left={"id": state_id, "resource_type": "ModelRevision"},
        right={"id": intermediate_mmt_id, "resource_type": "Intermediate"},
        relation_type="REINTERPRETS",
        user_id=1,
        url=args.url,
    )

    for concept in model_concepts:
        add_concept(concept=concept, object_id=model_id, type="models", url=args.url)

    ### upload model parameters ###
    print("Model Parameters")
    # load parameters of the model and set the type values
    create_model_parameters(
        path_parameters=f"{scenario}/model_mmt_parameters.json",
        path_initials=f"{scenario}/model_mmt_initials.json",
        model_id=model_id,
        url=args.url,
    )

    # ## set concept to inital model parameters
    # # get parameters
    response = requests.request("GET", args.url + f"models/{model_id}/parameters")
    parameters_model_json = response.json()

    with open(f"{scenario}/model_mmt_initials.json", "r") as f:
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
                            url=args.url,
                        )
                    if ido is not None:
                        add_concept(
                            concept=f"ido:{ido}",
                            object_id=parameter.get("id"),
                            type="model_parameters",
                            url=args.url,
                        )
