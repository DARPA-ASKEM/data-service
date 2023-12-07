# -*- coding: utf-8 -*-

import uuid
import time
from langchain.tools import tool
from langchain.agents import load_tools
import os
import json
import logging
import requests
from datetime import datetime
import re
from langchain.tools import StructuredTool

PROJECT_ID = 87 # Get project ID from environment, llm doesn't need to think about this
#TDS_URL = os.environ.get("TDS_URL", "http://data-service:8000")
TDS_URL ="https://data-service.staging.terarium.ai"
#PYCIEMSS_URL = os.environ.get("PYCIEMSS_URL", "http://pyciemss-api:8000")
PYCIEMSS_URL="https://pyciemss.staging.terarium.ai"
#SCIML_URL = os.environ.get("SCIML_URL", "http://sciml-service:8080")
SCIML_URL="www.SCIML.com"
WORKFLOW_ID = '36e62b6d-1fc2-440c-bb1a-6e5cce33d62a'


#llm won't use this for now, just use in setup
def add_workflow(workflow_payload,project_id=PROJECT_ID):
    workflow_response = requests.post(
        TDS_URL + "/workflows",
        json=workflow_payload,
        headers={"Content-Type": "application/json"},
    )
    if workflow_response.status_code >= 300:
        raise Exception(f"Failed to post workflow ({workflow_response.status_code})")
    else:
        add_asset(workflow_response.json()["id"], "workflows", project_id)
    return workflow_response
        
def create_project():
    '''
    Generate test project in TDS
    '''
    current_timestamp = datetime.now()
    ts = current_timestamp.strftime('%Y-%m-%d %H:%M:%S')

    project = {
        "name": "LLM Playground",
        "description": f"Project to try out LLM stuff",
        "assets": [],
        "active": True,
        }    

    resp = requests.post(f"{TDS_URL}/projects", json=project)
    project_id = resp.json()['id']

    return project_id   

#to do: put this more places to cover for weaker models' improper formatting
def remove_end_quotes(text):
    # Check if the first character is a quote
    if text.startswith(("'", '"')):
        text = text[1:]  # Remove the first character

    # Check if the last character is a quote
    if text.endswith(("'", '"')):
        text = text[:-1]  # Remove the last character

    return text
    
def get_project(project_id):
    resp = requests.get(f"{TDS_URL}/projects/{project_id}")
    return resp.json()

def get_project_assets(project_id):
    resp = requests.get(f"{TDS_URL}/projects/{project_id}/assets")
    return resp.json()

def get_model_configs(model_id):
    res=requests.get(
        TDS_URL + f"/models/{model_id}/model_configurations",
        headers={"Content-Type": "application/json"},
    )
    if res.status_code>300:
        return f'Invalid model id. Please try again with valid model id. Maybe you entered a model config id?'
    return res.json()
def get_model_information(model_id):
    res=requests.get(
        TDS_URL + f"/models/{model_id}",
        headers={"Content-Type": "application/json"},
    )
    if res.status_code>300:
        return f'Invalid model id. Please try again with valid model id. Maybe you entered a model config id? To lookup model config ids use the Lookup Model Configuration Information tool'
    return res.json()
def get_dataset_information(dataset_id):
    res=requests.get(
        TDS_URL + f"/datasets/{dataset_id}",
        headers={"Content-Type": "application/json"},
    )
    if res.status_code>300:
        return f'Invalid dataset id. Please try again with valid dataset id'
    return res.json()
def get_simulation_information(simulate_or_calibrate_id):
    res=requests.get(
        TDS_URL + f"/simulations/{simulate_or_calibrate_id}",
        headers={"Content-Type": "application/json"},
    )
    if res.status_code>300:
        return f'Invalid simulation/calibration id. Please try again with valid simulation/calibration id'
    return res.json()
def get_model_config(model_config_id):
    res=requests.get(
        TDS_URL + f"/model_configurations/{model_config_id}",
        headers={"Content-Type": "application/json"},
    )
    if res.status_code>300:
        return f'Invalid model config id. Please try again with valid model config id. Maybe you entered a model id? To lookup model ids use the Lookup Model Information tool'
    return res.json()

#simulate post
# {
#   "id": "str",
#   "execution_payload": {},
#   "result_files": [],
#   "type": "ensemble|simulation|calibration",
#   "status": "queued|running|complete|error|cancelled|failed",
#   "reason": "Only filled if simulation failed.",
#   "start_time": "timestamp",
#   "completed_time": "timestamp",
#   "engine": "ciemss|julia",
#   "workflow_id": "str",
#   "user_id": "int",
#   "project_id": "int"
# }

# simulate put
# {
#   "id": "str",
#   "execution_payload": {},
#   "result_files": [],
#   "type": "ensemble|simulation|calibration",
#   "status": "queued|running|complete|error|cancelled|failed",
#   "reason": "Only filled if simulation failed.",
#   "start_time": "timestamp",
#   "completed_time": "timestamp",
#   "engine": "ciemss|julia",
#   "workflow_id": "str",
#   "user_id": "int",
#   "project_id": "int"
# }

def modify_simulate_tds(simulate_id,simulate_payload,simulate_type):
    put_payload={
      "id": simulate_id,
      "execution_payload": simulate_payload,
      "result_files": [],
      "type": simulate_type,
      "status": "queued", #to do: change to other types later..
      "reason": "",
      "start_time": "", # to do: we aren't starting sims yet
      "completed_time": "", # to do: we aren't starting sims yet
      "engine": "ciemss", #to do: other options later?
      "workflow_id": WORKFLOW_ID,
      "user_id": "int",
      "project_id": PROJECT_ID
    }
    res = requests.put(
        TDS_URL + f"/simulations/{simulate_id}",
        json=simulate_payload,
        headers={"Content-Type": "application/json"},
    )
    #to do: add except...
    return res.json()
def add_model_config(config_payload):
    model_config_res = requests.post(
        TDS_URL + "/model_configurations",
        json=config_payload,
        headers={"Content-Type": "application/json"},
    )
    #to do: add except...
    return model_config_res.json()
#used to populate llm context and get context to add to for put
def get_workflow(workflow_id):
    workflow_response = requests.get(
        TDS_URL + f"/workflows/{workflow_id}",
        headers={"Content-Type": "application/json"},
    )
    if workflow_response.status_code==200:
        return workflow_response.json()
    else:
        return f'Failed to get workflow. Status Code:{workflow_response.status_code}.Error:{workflow_response.reason}'

def modify_workflow(workflow_payload,workflow_id):
    workflow_response = requests.put(
        TDS_URL + f"/workflows/{workflow_id}",
        json=workflow_payload,
        headers={"Content-Type": "application/json"},
    )
    if workflow_response.status_code >= 300:
        raise Exception(f"Failed to post workflow ({workflow_response.status_code})")
    else:
        if PROJECT_ID:
            project_id = PROJECT_ID
        else:
            with open("project_id.txt", "r") as f:
                project_id = f.read()
    new_workflow=get_workflow(workflow_id)
    return f"Workflow Successfully modified. New workflow:\n{new_workflow}"

def eval_integration(service_name, endpoint, request):
    start_time = time.time()
    is_success = False
    base_url = PYCIEMSS_URL if service_name == "pyciemss" else SCIML_URL
    sim_id = None
    kickoff_request = requests.post(
        f"{base_url}/{endpoint}",
        json=request,
        headers={"Content-Type": "application/json"},
    )
    logging.info(
        f"Kicked request: {kickoff_request.status_code} {kickoff_request.text}"
    )
    # if kickoff_request.status_code < 300:
    #     sim_id = kickoff_request.json()["simulation_id"]
    #     logging.info(f"Simulation ID: {sim_id}")
    #     get_status = lambda: requests.get(f"{base_url}/status/{sim_id}").json()[
    #         "status"
    #     ]
    #     while get_status() in ["queued", "running"]:
    #         time.sleep(1)
    #     if get_status() == "complete":
    #         logging.info(f"Completed status on simulation: {sim_id}")
    #         is_success = True
    #         # Add artifacts from simulations to TDS depending on what test is being run:
    #         # 1) Simulation in TDS
    #         add_asset(sim_id, "simulations", PROJECT_ID)
    add_asset(sim_id, "simulations", PROJECT_ID)
    return {
        "Integration Status": is_success,
        "Execution Time": time.time() - start_time,
    }, sim_id

def add_asset(resource_id, resource_type, project_id):
    if not project_id:
        try:
            with open('project_id.txt', 'r') as f:
                project_id = f.read()
        except:
            raise Exception("No PROJECT_ID found in environment and no project_id.txt file found")
    logging.info(f"Adding asset {resource_id} of type {resource_type} to project {project_id}")
    resp = requests.post(f"{TDS_URL}/projects/{project_id}/assets/{resource_type}/{resource_id}")
    if resp.status_code >= 300:
        logging.error(f"Failed to add asset to project: status - {resp.status_code}: {resp.json()}")
        return resp.json()
    
    provenance_payload = {
        "relation_type": "CONTAINS",
        "left": project_id,
        "left_type": "Project",
        "right": resource_id,
        "right_type": resource_type[:-1].capitalize(), # Converts "models" to "Model", etc.
    }
    prov_resp = requests.post(f"{TDS_URL}/provenance", json=provenance_payload)

    if prov_resp.status_code >= 300:
        logging.error(f"Failed to add provenance for project CONTAINS {resource_type}: status - {prov_resp.status_code}: {prov_resp.json()}")
    return resp.json()


def generate_workflow(workflow_name, workflow_description):
    workflow_id = str(uuid.uuid4())
    workflow_payload = {
        "id": workflow_id,
        "name": workflow_name,
        "description": workflow_description,
        "transform": {"x": 0, "y": 0, "k": 1},
        "nodes": [],
        "edges": [],
    }

    return workflow_payload, workflow_id


def generate_model_module(model_id, workflow_id, model_config_id=None,model_label=None):
    model_module_uuid = str(uuid.uuid4())
    config_output_uuid = str(uuid.uuid4())
    default_config_output_uuid = str(uuid.uuid4())
    if not model_label:model_label=model_config_id
    model_payload = {
        "id": model_module_uuid,
        "workflowId": workflow_id,
        "operationType": "ModelOperation",
        "displayName": "Model",
        "x": 400,
        "y": 150,
        "state": {"modelId": model_id, "modelConfigurationIds": [model_config_id]},
        "inputs": [],
        "outputs": [
            {
                "id": config_output_uuid,
                "type": "modelConfigId",
                "label": model_label,
                "value": [model_config_id],
                "status": "not connected",
            },
        ],
        "statusCode": "valid",
        "width": 180,
        "height": 220,
    }

    return (
        model_payload,
        model_module_uuid,
        config_output_uuid,
        default_config_output_uuid,
    )


def generate_dataset_module(dataset_id, workflow_id):
    module_uuid = str(uuid.uuid4())

    dataset_output_uuid = str(uuid.uuid4())

    dataset_module_payload = {
        "id": module_uuid,
        "workflowId": workflow_id,
        "operationType": "Dataset",
        "displayName": "Dataset",
        "x": 375,
        "y": 550,
        "state": {"datasetId": dataset_id},
        "inputs": [],
        "outputs": [
            {
                "id": dataset_output_uuid,
                "type": "datasetId",
                "label": dataset_id,
                "value": [dataset_id],
                "status": "not connected",
            }
        ],
        "statusCode": "invalid",
        "width": 180,
        "height": 220,
    }

    return dataset_module_payload, module_uuid, dataset_output_uuid


def generate_calibrate_simulate_ciemms_module(
    workflow_id, config_id, dataset_id, simulation_output,timespan,extra
):
    module_uuid = str(uuid.uuid4())

    config_uuid = str(uuid.uuid4())
    dataset_uuid = str(uuid.uuid4())
    sim_output_uuid = str(uuid.uuid4())

    module_payload = {
        "id": module_uuid,
        "workflowId": workflow_id,
        "operationType": "CalibrationOperationCiemss",
        "displayName": "Calibrate & Simulate (probabilistic)",
        "x": 1100,
        "y": 200,
        "state": {
            "chartConfigs": [
                {"selectedRun": simulation_output, "selectedVariable": []}
            ],
            "mapping": [{"modelVariable": "", "datasetVariable": ""}],
            "simulationsInProgress": [],
            "timeSpan": timespan,
            "extra": extra,
        },
        "inputs": [
            {
                "id": config_uuid,
                "type": "modelConfigId",
                "label": config_id,
                "status": "connected",
                "value": [config_id],
            },
            {
                "id": dataset_uuid,
                "type": "datasetId",
                "label": dataset_id,
                "status": "connected",
                "value": [dataset_id],
            },
        ],
        "outputs": [
            {
                "id": sim_output_uuid,
                "type": "number",
                "label": "Output 1",
                "value": [{"runId": simulation_output}],
                "status": "not connected",
            }
        ],
        "statusCode": "invalid",
        "width": 420,
        "height": 220,
    }

    return module_payload, module_uuid, config_uuid, dataset_uuid


def generate_simulate_ciemms_module(workflow_id, config_id, simulation_output,timespan, extra):
    module_uuid = str(uuid.uuid4())

    config_uuid = str(uuid.uuid4())
    sim_output_uuid = str(uuid.uuid4())
    num_samples=100
    if "num_samples" in extra.keys():
        num_samples=extra["num_samples"]
    module_payload = {
        "id": module_uuid,
        "workflowId": workflow_id,
        "operationType": "SimulateCiemssOperation",
        "displayName": "Simulate (probabilistic)",
        "x": 1100,
        "y": 500,
        "state": {
            "simConfigs": {
                "runConfigs": {
                    simulation_output: {
                        "runId": simulation_output,
                        "active": True,
                        "configName": "Model configuration",
                        "timeSpan": timespan,
                        "numSamples": num_samples,
                        "method": "dopri5",
                    }
                },
                "chartConfigs": [],
            },
            "currentTimespan": timespan,
            "extra": extra,
            "numSamples": num_samples,
            "method": "dopri5",
            "simulationsInProgress": [],
        },
        "inputs": [
            {
                "id": config_uuid,
                "type": "modelConfigId",
                "label": config_id,
                "status": "connected",
                "value": [config_id],
                "acceptMultiple": False,
            }
        ],
        "outputs": [
            {
                "id": sim_output_uuid,
                "type": "simOutput",
                "label": "Output 1",
                "value": [simulation_output],
                "status": "not connected",
            }
        ],
        "status": "invalid",
        "width": 420,
        "height": 220,
    }
        

    return module_payload, module_uuid, config_uuid


def generate_edge(workflow_id, source_id, target_id, source_port, target_port):
    edge_uuid = str(uuid.uuid4())
    edge_payload = {
        "id": edge_uuid,
        "workflowId": workflow_id,
        "source": source_id,
        "sourcePortId": source_port,
        "target": target_id,
        "targetPortId": target_port,
        "points": [
            {
                "x": 0,
                "y": 0,
            },
            {
                "x": 0,
                "y": 0,
            },
        ],
    }
    return edge_payload, edge_uuid

def clear_workflow():
    workflow_id = WORKFLOW_ID
    workflow_payload=get_workflow(workflow_id)
    workflow_payload['nodes'],workflow_payload['edges']=[],[]
    modify_workflow(workflow_payload,workflow_id)
    
@tool("Create Project")
def create_project_tool():
    """
    Create a project to put new workflows and assets into.
    A project in Terarium is a self-contained set of assets (models, workflows, simulations, calibrations, etc..) and workflows using those assets.
    This project will automatically be used in creating future workflows and nodes and edges in that workflow.
    
    Parameters
    ----------
    No input parameters required
        
    Returns
    ----------
        string indicating action success and the new project id or failure.

    """
    project_id=create_project()
    #to do: set os.env
    return f'Project succesfully created. Project ID is {project_id}'

# def search_user_current_projects:
    
    
@tool("Create Workflow")
def create_workflow_tool(workflow_name:str, workflow_description:str,project_id:int=PROJECT_ID):
    """
    Create a workflow to perform actions on assets(models, workflows, simulations, calibrations, etc..).
    To create a workflow you will need to first create a project if one does not exist or is not specified. 
    If the user does not specify the workflow name or description when attempting to create a workflow, use the Ask User tool to ask them for a workflow name and description
    This workflow will automatically be used as the default workflow until another workflow is created.
    
    Parameters
    ----------
    workflow_name (str): The name of the workflow.
    workflow_description (str) : A description of the workflow
    project_id (int): The id of the project under which to create this workflow. Defaults to PROJECT_ID Variable.
        
    Returns
    ----------
        string indicating action success and the new project id or failure.

    """
    workflow_payload,workflow_id=generate_workflow(workflow_name,workflow_description)
    workflow_response=add_workflow(workflow_payload,project_id=project_id)
    workflow_id=workflow_response.json()["id"]
    return f'Workflow succesfully created. Workflow ID is {workflow_id}'
    

@tool("Add Model to Workflow")
def add_model(model_id:str):
    """
    Add an existing model in the Terarium Data Service to the current Terarium workflow.
    Populates the model with the default config if it exists.
    You need a model id to use this function. You can get model ids by searching the Terrarium Data Service database for models using the Search for Models tool.
    The input to this tool should be a single string like "model_id"
    
    Parameters
    ----------
        model_id (str) : The model id of the model which is going to be added.
        
    Returns
    ----------
        string indicating action success and new workflow information or failure.

    """
    #call tds apis
    workflow_id = WORKFLOW_ID
    project_id=PROJECT_ID
    workflow_payload=get_workflow(workflow_id) #get from env
    #add exception to remove duplicate models or just modify models in place if we try to create a super similar model
    #get default config if it exists
    model_configs=get_model_configs(model_id)
    model_config_id=None
    model_label=None
    for config in model_configs:
        if 'default' in config['name'].lower():
            model_config_id=config['id']
            model_label=config['name']
            break
    if not model_config_id:
        model_config_id=model_configs[0]['id']
        model_label=model_configs[0]['name']
    (
        model_payload,
        model_module_uuid,
        config_output_uuid,
        default_config_output_uuid,
    ) = generate_model_module(model_id=model_id,workflow_id=workflow_id,model_config_id=model_config_id,model_label=model_label)
    workflow_payload['nodes'].append(model_payload)
    res=modify_workflow(workflow_payload,workflow_id)
    add_asset(model_id, "models", PROJECT_ID)
    return res

#You can get dataset ids by searching the Terarium Data Service database for models using the Search for Models tool.
#example dataset for now, id = "covid-19-us-data"
@tool("Add Dataset to Workflow")
def add_dataset(dataset_id:str):
    """
    Add an existing dataset in the Terarium Data Service to the current Terarium workflow.
    You need a dataset id to use this function. The user should give you the dataset id.
    
    Parameters
    ----------
        dataset_id (str) : The Terarium Data Service id of the dataset which is going to be simulated.
        
    Returns
    ----------
        string indicating action success and new workflow information or failure.

    """
    #call tds apis
    workflow_id = WORKFLOW_ID
    project_id=PROJECT_ID
    workflow_payload=get_workflow(workflow_id) #get from env
    #add exception to remove duplicate datasets or just modify datasets in place if we try to create a super similar dataset
    (
        dataset_payload,
        dataset_module_uuid,
        dataset_output_uuid,
    ) = generate_dataset_module(dataset_id, workflow_id)

    workflow_payload["nodes"].append(dataset_payload)
    res=modify_workflow(workflow_payload,workflow_id)
    add_asset(dataset_id, "datasets", PROJECT_ID)
    return res

def add_simulation(model_config_id:str,simulation_settings:dict=None):
    """
    Adds a new simulation module to the current Terarium workflow.
    A simulation module takes a model configuration and simulates the model associated with that model configuration with the particular configuration enabled.
    To use this function you will need a model config id, which can be found in the workflow id 
    Parameters
    ----------
        model_config_id (str) : The id of the model configuration which is going to be simulated, can be found in the workflow dictionary.
        simulation_settings (dict) : a dictionary of simulation settings in the form of  
        {{
              "timespan": {{
                "start": 0,
                "end": 90
              }},
              "extra": {{
                "num_samples": 100
              }}
            }}
        Each dictionary (timespan and extras) can optionally be included. Each key in extras can be used independently as well.
        
    Returns
    ----------
        string indicating action success or failure.
    """
    workflow_id = WORKFLOW_ID
    workflow_payload=get_workflow(workflow_id)
    #get model tds based on model config
    model_config_tds_id=None
    associated_model_tds_id=None
    associated_model_workflow_id=None
    for node in workflow_payload['nodes']:
        for output in node['outputs']:
            if output['id']==model_config_id or output['value'][0]==model_config_id: #correct tds/workflow id mixups
                model_config_tds_id=output['value'][0]
                model_config_id=output['id']
                associated_model_workflow_id=node['id']
                model_config=get_model_config(model_config_tds_id)
                associated_model_tds_id=model_config['model_id']
                
                
    #example simulate for sidarthe
    #     {
    #   "engine": "ciemss",
    #   "username": "not_provided",
    #   "model_config_id": "sidarthe",
    #   "timespan": {
    #     "start": 0,
    #     "end": 90
    #   },
    #   "extra": {
    #     "num_samples": 100
    #   }
    # }
    simulation_dictionary= {
          "engine": "ciemss",
          "username": "not_provided",
          "model_config_id": model_config_tds_id, #model tds or model config tds?
          "timespan": {
            "start": 0,
            "end": 90
          },
          "extra": {
            "num_samples": 100
          }
        }
    if simulation_settings: simulation_dictionary.update(simulation_settings)
    
    success,simulation_output = eval_integration("pyciemss", "simulate", simulation_dictionary) #options from endpoint are calibrate,optimize-calibrate,optimize-simulate,simulate
    
    (
        simulate_ciemss_payload,
        simulate_ciemss_uuid,
        config_input_uuid,
    ) = generate_simulate_ciemms_module(
        workflow_id, model_config_tds_id, simulation_output,simulation_dictionary["timespan"],simulation_dictionary["extra"] #model tds or model config tds?
    )
    workflow_payload["nodes"].append(simulate_ciemss_payload)
    config_output_uuid = str(uuid.uuid4())
    model_simulate_edge, model_simulate_edge_uuid = generate_edge(
        workflow_id,
        associated_model_workflow_id,
        simulate_ciemss_uuid,
        model_config_id,
        config_input_uuid,
    )
    for i,node in enumerate(workflow_payload['nodes']):
        for j,output in enumerate(node["outputs"]):
            if output['id']==model_config_id:
               workflow_payload['nodes'][i]["outputs"][j]['status']="connected"
    workflow_payload["edges"].append(model_simulate_edge)
    res=modify_workflow(workflow_payload, workflow_id)
    return f"Simulation node was added to the workflow. {res}"

add_simulation_tool = StructuredTool.from_function(add_simulation)
add_simulation_tool.name="Add Simulation module to Workflow"

# def edit_simulation(model_config_id:str,simulation_settings:dict=None):
#     """
#     Adds a new simulation module to the current Terarium workflow.
#     A simulation module takes a model configuration and simulates the model associated with that model configuration with the particular configuration enabled.
#     To use this function you will need a model config id, which can be found in the workflow id 
#     Parameters
#     ----------
#         model_config_id (str) : The id of the model configurationwhich is going to be simulated, can be found in the workflow dictionary.
#         simulation_settings (dict) : a dictionary of simulation settings in the form of  
#         {{
#               "timespan": {{
#                 "start": 0,
#                 "end": 90
#               }},
#               "extra": {{
#                 "num_samples": 100
#               }}
#             }}
#         Each dictionary (timespan and extras) can optionally be included. Each key in extras can be used independently as well.
        
#     Returns
#     ----------
#         string indicating action success or failure.
#     """
#     workflow_id = WORKFLOW_ID
#     workflow_payload=get_workflow(workflow_id)
#     #get model tds based on model config
#     model_config_tds_id=None
#     associated_model_tds_id=None
#     associated_model_workflow_id=None
#     for node in workflow_payload['nodes']:
#         for output in node['outputs']:
#             if output['id']==model_config_id:
#                 model_config_tds_id=output['value'][0]
#                 associated_model_workflow_id=node['id']
#                 model_config=get_model_config(model_config_tds_id)
#                 associated_model_tds_id=model_config['model_id']
                
                
#     #example simulate for sidarthe
#     #     {
#     #   "engine": "ciemss",
#     #   "username": "not_provided",
#     #   "model_config_id": "sidarthe",
#     #   "timespan": {
#     #     "start": 0,
#     #     "end": 90
#     #   },
#     #   "extra": {
#     #     "num_samples": 100
#     #   }
#     # }
#     simulation_dictionary= {
#           "engine": "ciemss",
#           "username": "not_provided",
#           "model_config_id": associated_model_tds_id, #model tds or model config tds?
#           "timespan": {
#             "start": 0,
#             "end": 90
#           },
#           "extra": {
#             "num_samples": 100
#           }
#         }
#     if simulation_settings: simulation_dictionary.update(simulation_settings)
    
#     success,simulation_output = eval_integration("pyciemss", "simulate", simulation_dictionary) #options from endpoint are calibrate,optimize-calibrate,optimize-simulate,simulate
    
#     (
#         simulate_ciemss_payload,
#         simulate_ciemss_uuid,
#         config_input_uuid,
#     ) = generate_simulate_ciemms_module(
#         workflow_id, associated_model_tds_id, simulation_output,simulation_dictionary #model tds or model config tds?
#     )
#     workflow_payload["nodes"].append(simulate_ciemss_payload)
#     config_output_uuid = str(uuid.uuid4())
#     model_simulate_edge, model_simulate_edge_uuid = generate_edge(
#         workflow_id,
#         associated_model_workflow_id,
#         simulate_ciemss_uuid,
#         model_config_id,
#         config_input_uuid,
#     )
#     workflow_payload["edges"].append(model_simulate_edge)
#     res=modify_workflow(workflow_payload, workflow_id)
#     return f"Simulation node was added to the workflow. {res}"

# edit_simulation_tool = StructuredTool.from_function(edit_simulation)
# edit_simulation_tool.name="Edit Simulation Node"

def add_calibration(model_config_id:str,dataset_id:str,mappings:dict,calibration_settings:dict=None):
    
    """
    Adds a new calibration/simulation node to the current Terarium workflow.
    This node first calibrates a model configuration based on relevant variables in a dataset which must be associated to model configuration states via a mapping dictionary.
    If you are unsure of how to map the model and dataset variables to each other, make your best guess and use the Ask User tool to ask the user if the mapping is correct.
    Make sure to provide the model variables and the dataset variables to the user when you ask, you can get these using the Lookup Model Information and Lookup Dataset Information tools respectively.
    It then simulates the associated model using the calibrated model configuration.
    
    Parameters
    ----------
        model_config_id (str) : The id of the model configurationwhich is going to be simulated, can be found in the workflow dictionary.
        dataset_id (str) : The node id of the dataset which is going to be used to calibrate the model configuration in the workflow dictionary.
        mappings: (dict) : A dictionary that maps names of variables in the dataset to names of the same variable in the model state which are going to be calibrated by the dataset, along with the timestep column as well..
        For example. If we have a dataset with columns ['tstep','S'] and model variables ['Timestep','Infected','Recovered','Susceptible'], we would make a mapping - 
        {{'tstep':'Timestep','S':'Susceptible'}}
        Note that mappings are key value pairs where the key is a dataset variable name and the key is a single model variable name and that mappings MUST INCLUDE A TIME VARIABLE.
        calibration_settings (dict) : a dictionary of settings in the form of  
          {{"timespan": {{
            "start": 0,
            "end": 90
          }},
          "extra": {{
            "num_samples": 100,
            "start_time": -1e-10,
            "num_iterations": 1000,
            "lr": 0.03,
            "verbose": false,
            "num_particles": 1,
            "method": "dopri5"
          }}
        }}
         which affects the calibration and simulation steps of this node.
        Each dictionary (timespan and extra) can optionally be included. Each key in extra can be used independently as well.
        If keys not included, they will set to the default above.
        
    Returns
    ----------
        string indicating action success or failure.
    """
    
    workflow_id = WORKFLOW_ID
    workflow_payload=get_workflow(workflow_id)
    #checks to see if the agent accidentally provided a tds dataset id
    dataset_id=remove_end_quotes(dataset_id)
    for node in workflow_payload['nodes']:
        if 'datasetId' in node['state'].keys():
            if node['state']['datasetId']==dataset_id:
                dataset_id=node['id']
    model_config_tds_id=None
    associated_model_tds_id=None
    associated_model_workflow_id=None
    dataset_workflow_output_id=None
    for node in workflow_payload['nodes']:
        for output in node['outputs']:
            if output['id']==model_config_id or output['value'][0]==model_config_id:
                model_config_tds_id=output['value'][0]
                model_config_id=output['id']
                associated_model_tds_id=node['state']['modelId']
        if 'datasetId' in node['state'].keys():
            if node['id']==dataset_id or node['state']['datasetId']==dataset_id:
                dataset_tds_id=node['state']['datasetId']
                dataset_output_uuid=node['outputs'][0]['id']
                associated_dataset_payload=get_dataset_information(dataset_tds_id)
                dataset_file_name=associated_dataset_payload['file_names'][0]
    #to do: add state changes?
    #get dataset file name from tds -         
    #example calibrate for sidarthe
    # {
    #   "engine": "ciemss",
    #   "username": "not_provided",
    #   "model_config_id": "sidarthe",
    #   "dataset": {
    #     "id": "traditional",
    #     "filename": "traditional.csv",
    #     "mappings": {
    #       "tstep": "Timestamp",
    #       "S": "Susceptible"
    #     }
    #   },
    #   "timespan": {
    #     "start": 0,
    #     "end": 90
    #   },
    #   "extra": {
    #     "num_samples": 100,
    #     "start_time": -1e-10,
    #     "num_iterations": 1000,
    #     "lr": 0.03,
    #     "verbose": false,
    #     "num_particles": 1,
    #     "method": "dopri5"
    #   }
    # }
    
    calibration_dictionary= {
      "engine": "ciemss",
      "username": "",
      "model_config_id": model_config_tds_id, #tds id or id in workflow dict??
      "dataset": {
        "id": dataset_id,
        "filename": dataset_file_name,
      },
      "timespan": {
        "start": 0,
        "end": 90
      },
      "extra": {
        "num_samples": 100,
        "start_time": -1e-10,
        "num_iterations": 1000,
        "lr": 0.03,
        "verbose": False,
        "num_particles": 1,
        "method": "dopri5"
      }
    }
    calibration_dictionary['dataset']['mappings']=mappings
    if calibration_settings: calibration_dictionary.update(calibration_settings)
    
    success,simulation_output = eval_integration("pyciemss", "calibrate", calibration_dictionary) #options from endpoint are calibrate,optimize-calibrate,optimize-simulate,simulate

    (
            calibrate_simulate_payload,
            calibrate_simulation_uuid,
            config_input_uuid, #model config workflow id
            dataset_input_uuid,
    ) = generate_calibrate_simulate_ciemms_module(
        workflow_id, model_config_tds_id, dataset_tds_id, simulation_output,calibration_dictionary["timespan"],calibration_dictionary["extra"] #tds ids for model, dataset, sim
    )
    workflow_payload["nodes"].append(calibrate_simulate_payload)
    #to do: modify node ['state']['mappings']??
    model_simulate_edge, model_simulate_edge_uuid = generate_edge(
        workflow_id,
        associated_model_workflow_id,
        calibrate_simulation_uuid,
        model_config_id, #model config (output uuid from model node)
        config_input_uuid, #simulate config input uuid
    )
    for i,node in enumerate(workflow_payload['nodes']):
        for j,output in enumerate(node["outputs"]):
            if output['id']==model_config_id:
               workflow_payload['nodes'][i]["outputs"][j]['status']="connected"
               
    workflow_payload["edges"].append(model_simulate_edge)

    dataset_simulate_edge, dataset_simulate_edge_uuid = generate_edge(
        workflow_id,
        dataset_id,
        calibrate_simulation_uuid,
        dataset_output_uuid,
        dataset_input_uuid, #simulate dataset input uuid
    )
    for i,node in enumerate(workflow_payload['nodes']):
        for j,output in enumerate(node["outputs"]):
            if output['id']==dataset_output_uuid:
               workflow_payload['nodes'][i]["outputs"][j]['status']="connected"
               
    workflow_payload["edges"].append(dataset_simulate_edge)

    res=modify_workflow(workflow_payload, workflow_id)
    return f"Calibration node was added to the workflow. {res}"

add_calibrate_tool = StructuredTool.from_function(add_calibration)
add_calibrate_tool.name="Add Calibration module to Workflow"

def edit_calibration(calibration_id:str,model_config_id:str=None,dataset_id:str=None,mappings:dict=None,calibration_settings:dict=None):
    
    """
    Edits an existing a new calibration/simulation node to the current Terarium workflow.
    If you want to edit the model 
    If you are unsure of how to map the model and dataset variables to each other, make your best guess and use the Ask User tool to ask the user if the mapping is correct.
    Make sure to provide the model variables and the dataset variables to the user when you ask, you can get these using the Lookup Model Information and Lookup Dataset Information tools respectively.
    It then simulates the associated model using the calibrated model configuration.
    
    Parameters
    ----------
        calibration_id (str): The id of the calibration node that you want to edit.
        model_config_id (str): The id of the model_config to attach to the simulation. Replaces the old model config.
        dataset_id (str): The id of the dataset to attach to the simulation. Replaces the old dataset
        mappings: (dict) : A dictionary that maps names of variables in the dataset to names of the same variable in the model state which are going to be calibrated by the dataset, along with the timestep column as well..
        For example. If we have a dataset with columns ['tstep','S'] and model variables ['Timestep','Infected','Recovered','Susceptible'], we would make a mapping - 
        {{'tstep':'Timestep','S':'Susceptible'}}
        Note that mappings are key value pairs where the key is a dataset variable name and the key is a single model variable name.
        calibration_settings (dict) : a dictionary of settings in the form of  
          {{"timespan": {{
            "start": 0,
            "end": 90
          }},
          "extra": {{
            "num_samples": 100,
            "start_time": -1e-10,
            "num_iterations": 1000,
            "lr": 0.03,
            "verbose": false,
            "num_particles": 1,
            "method": "dopri5"
          }}
        }}
          which affects the calibration and simulation steps of this node.
        Each dictionary (timespan and extra) can optionally be included. Each key in extra can be used independently as well.
        If keys not included, they will set to the default above.
        
    Returns
    ----------
        string indicating action success or failure.
    """
    
    workflow_id = WORKFLOW_ID
    workflow_payload=get_workflow(workflow_id)
    calibration_payload=get_simulation_information(calibration_id)
    calibration_dictionary=calibration_payload['settings'] #change to real
    
    #checks to see if the agent accidentally provided a tds dataset id
    dataset_id=remove_end_quotes(dataset_id)
    for node in workflow_payload['nodes']:
        if 'datasetId' in node['state'].keys():
            if node['state']['datasetId']==dataset_id:
                dataset_id=node['id']
                   
    #to do: add state changes?
    #get dataset file name from tds -
    #to do: modify node ['state']['mappings']??
    model_config_tds_id=None
    associated_model_tds_id=None
    associated_model_workflow_id=None
    dataset_workflow_output_id=None
    if model_config_id:
        for node in workflow_payload['nodes']:
            for output in node['outputs']:
                if output['id']==model_config_id:
                    model_config_tds_id=output['value'][0]
                    associated_model_tds_id=node['state']['modelId']
                    
    if dataset_id:  
        for node in workflow_payload['nodes']:             
            if node['id']==dataset_id:
                dataset_tds_id=node['state']['datasetId']
                dataset_output_uuid=node['outputs'][0]['id']
                associated_dataset_payload=get_dataset_information(dataset_tds_id)
                dataset_file_name=associated_dataset_payload['file_names'][0]
    if mappings:calibration_dictionary['dataset']['mappings']=mappings
    if calibration_settings: calibration_dictionary.update(calibration_settings)
    calibration_payload['settings']=calibration_dictionary
    modify_simulate_tds(calibration_payload)
    #change workflow_payload
    for i,node in enumerate(workflow_payload['nodes']):
        if node['id']==calibration_id:
            workflow_payload['nodes'][i]=calibration_payload
    res=modify_workflow(workflow_payload, workflow_id)
    return f"Calibration node was successfully modified. {res}"

edit_calibrate_settings_tool = StructuredTool.from_function(edit_calibration)
edit_calibrate_settings_tool.name="Edit Calibration Node"

@tool("Lookup Model Information")
def lookup_model(model_id:str):
    """
    Look up information on a model by its model_id such as its state variables and parameters using the Terarium Data Service.
    Do not have any quotes on either end of the model id. Ie. '4353ba5a-9b40-44d2-8233-05911b250aa1' bad, 4353ba5a-9b40-44d2-8233-05911b250aa1 good.
    Parameters
    ----------
        model_id (str) : The model id of the model which is to be looked up. ex. 4353ba5a-9b40-44d2-8233-05911b250aa1
        
    Returns
    ----------
        string indicating model information

    """
    workflow_id = WORKFLOW_ID
    workflow_payload=get_workflow(workflow_id)
    #checks to see if the agent accidentally provided a workflow model uuid
    model_id=remove_end_quotes(model_id)
    model_tds_id=model_id
    for node in workflow_payload['nodes']:
        if node['id']==model_id:
            model_tds_id=node['state']['modelId']
    res=get_model_information(model_tds_id)
    return json.dumps(res)

@tool("Lookup Dataset Information")
def lookup_dataset(dataset_id:str):
    """
    Look up information on a dataset by its dataset_id such as its state variables and parameters using the Terarium Data Service.
    Do not have any quotes on either end of the dataset id. Ie. '4353ba5a-9b40-44d2-8233-05911b250aa1' bad, 4353ba5a-9b40-44d2-8233-05911b250aa1 good.
    Parameters
    ----------
        dataset_id (str) : The dataset id of the dataset which is to be looked up. ex. 4353ba5a-9b40-44d2-8233-05911b250aa1
        
    Returns
    ----------
        string indicating dataset information

    """
    workflow_id = WORKFLOW_ID
    workflow_payload=get_workflow(workflow_id)
    #checks to see if the agent accidentally provided a workflow dataset uuid
    dataset_id=remove_end_quotes(dataset_id)
    dataset_tds_id=dataset_id
    for node in workflow_payload['nodes']:
        if node['id']==dataset_id:
            dataset_tds_id=node['state']['datasetId']
    res=get_dataset_information(dataset_tds_id)

    return json.dumps(res)

@tool("Lookup Model Configuration Information")
def lookup_model_config(model_config_id:str):
    """
    Look up information on a model configuration by its id such as its state variables and parameters using the Terarium Data Service.
    Do not have any quotes on either end of the model id. Ie. '4353ba5a-9b40-44d2-8233-05911b250aa1' bad, 4353ba5a-9b40-44d2-8233-05911b250aa1 good.
    
    Parameters
    ----------
        model_config_id (str) : The id of the model configuration which is to be looked up. ex: 4353ba5a-9b40-44d2-8233-05911b250aa1
        
    Returns
    ----------
        string indicating model configuration information

    """
    workflow_id = WORKFLOW_ID
    workflow_payload=get_workflow(workflow_id)
    model_config_id=remove_end_quotes(model_config_id) #remove accidental strings
    model_config_tds_id=model_config_id
    #check to see if the agent gave the wrong id and correct it if it did
    for node in workflow_payload['nodes']:
        for output in node['outputs']:
            if output['id']==model_config_id:
                model_config_tds_id=output['value'][0]
        
    res=get_model_config(model_config_tds_id)
    return json.dumps(res)

@tool("Search for Models")
def search_models(query:str):
    """
    Searches for models in the Terrarium Data Service database that are relevant for the query and returns the top 10 results along with information on those top 10 models.
    Use this tool when the user asks you to look for a model and return the results to the user in a easy to understand format including the model name and description and any other information about the models which you think will be helpful and ask them which one they want to use. 
    
    Parameters
    ----------
        query (str) : Plain Text Query to find relevant models
        
    Returns
    ----------
        string returning either list of relevant models in order of relevance and brief model info or error message

    """
    elasticsearch_payload={"multi_match": {
      "query": query,
      "fields": ["header.name", "header.description"]
      }
    }
    search_response = requests.post(
        TDS_URL + "/models/search",
        json=elasticsearch_payload,
        headers={"Content-Type": "application/json"},
    )
    if search_response.status_code==200:
        return f"Found models relevant to your query.\nModels:\n{search_response.json()}"
    else:
        return f"Error in request:Code:{search_response.status_code}.Reason:{search_response.reason}"

#maybe add missing inputs in config on error?
#add automatic response to agent reply in cli?
# @tool("Create Model Configuration for Existing Model")
#    For example, suppose the user said, Gamma should be 0.2 and the rest of the parameters can be left as default and we could assume they were referring to the only model in the workflow which had a model id of '1234', in this case our input to this function would be model_id='1234',parameters_dict={{"Gamma":0.2}}
def edit_model_config(model_id:str,model_config_id:str=None,parameters_dict:dict=None,initials_dict:dict=None):
    """
    Creates a new model configuration by modifying values in an existing configuration in the current Terrarium workflow.
    Usually a user will specific a few parameters in a model configuration that they will want to change.
    Note that the user may use natural language which does not exactly match the parameter names of the model config. You should use the lookup_model_config before using tool to find the model config options to determine which variables the user is referring to.
    In that case provide the id of the model associated with the model configuration and a dictionary of the parameters that are going to change.
    
    Parameters
    ----------
        model_id (str) : The id of the model with which the model configuration is associated in the workflow dictionary. This refers to the id in the workflow dictionary, not the id of the model in tds. ie. 
        model_config_id (str) : The id of the model configuration to start from. If None, uses default config associated with model id.
        parameters_dict (dict): Dict of parameters to change in the model configuration along with their new values. Values should be floats. This is optional.
        initials_dict (dict): Dict of model initial condition variables to change in the model configuration along with their values.Values should be strings where the strings are floats., ie '0.95'. This is optional.
    Returns
    ----------
        string indicating action success and the resulting new workflow or failure

    """
    #to do: check if requested model configuration is valid, if not ask the user if they want to change the minimum and maximum parameter range to allow it?
    #ie. this field in the model config -               "parameters": {"minimum": 0.01,"maximum": 0.5}
    workflow_id = WORKFLOW_ID
    workflow_payload=get_workflow(workflow_id)
    #checks to see if the agent accidentally provided a tds model id
    model_id=remove_end_quotes(model_id)
    for node in workflow_payload['nodes']:
        if 'modelId' in node['state'].keys():
            if node['state']['modelId']==model_id:
                model_id=node['id']
                
    model_tds_id=[node['state']['modelId'] for node in workflow_payload['nodes'] if node['id']==model_id][0]
    model_configs=get_model_configs(model_tds_id)
    if not model_config_id:
        for config in model_configs:
            if 'default' in config['name'].lower():
                model_config_id=config['id']
                model_label=config['name']
                #to do: add check to make sure model config is in workflow, if not add it
                break
    if not model_config_id:
        model_config_id=model_configs[0]['id']
        model_label=model_configs[0]['name']
    model_config_payload=get_model_config(model_config_id)
    if parameters_dict:
        for key in parameters_dict:
            valid_key=False
            for i,item in enumerate(model_config_payload['configuration']['semantics']['ode']['parameters']):
                if item['id']==key:
                    model_config_payload['configuration']['semantics']['ode']['parameters'][i].update({'value':parameters_dict[key]})
                    valid_key=True
            if not valid_key:
                return f"Model Configuration was not created. Tell the user that the {key} parameter is not a parameter in the model and that the valid parameters are {[item['id'] for item in model_config_payload['configuration']['semantics']['ode']['parameters']]}"
    if initials_dict:
        for key in initials_dict:
            valid_key=False
            for i,item in enumerate(model_config_payload['configuration']['semantics']['ode']['initials']):
                if item['target']==key:
                    model_config_payload['configuration']['semantics']['ode']['initials'][i].update({'expression':initials_dict[key]})
                    floaty=re.findall(r'[-+]?[0-9]*\.?[0-9]+', item['expression_mathml'])[0]
                    model_config_payload['configuration']['semantics']['ode']['initials'][i].update({'expression_mathml':item['expression_mathml'].replace(floaty,initials_dict[key])})
                    valid_key=True
            if not valid_key:
                return f"Model Configuration was not created. Tell the user that the {key} state variable is not a variable in the model and that the valid state variables are {[item['target'] for item in model_config_payload['configuration']['semantics']['ode']['initials']]}"
    model_config_payload.pop('id')
    config_uuid=str(uuid.uuid4())
    model_config_payload['name']=config_uuid
    model_config_payload['description']=model_config_payload['description']+ ' Modified'
    new_model_config_id=add_model_config(model_config_payload)['id'] #create model config in tds
    for i,node in enumerate(workflow_payload['nodes']):
        if node['id']==model_id:
            workflow_payload['nodes'][i]['state']['modelConfigurationIds'].append(new_model_config_id)
            
            workflow_payload['nodes'][i]['outputs'].append({'id': config_uuid,
              'type': 'modelConfigId',
              'label': new_model_config_id,
              'value': [new_model_config_id],
              'status': "not connected"})
    res=modify_workflow(workflow_payload, workflow_id)
    return f"Model Configuration was created and changed to active config for the model in the workflow. {res}"

edit_model_config_tool = StructuredTool.from_function(edit_model_config)
edit_model_config_tool.name="Create Model Configuration for Existing Model"

@tool("Remove Node")
def remove_node(node_id:str):
    """
    Removes a node from the current workflow with a given id
    You can find the id of the node to be removed in the dictionary of the current workflow.
    
    Parameters
    ----------
        node_id (str) : The id of the node to be deleted in the workflow dictionary
        
    Returns
    ----------
        string indicating action success and the resulting new workflow or failure

    """
    workflow_id = WORKFLOW_ID
    workflow_payload=get_workflow(workflow_id)
    for i,node in enumerate(workflow_payload['nodes']):
        if node['id']==node_id:
            workflow_payload['nodes'].pop(i)
    res=modify_workflow(workflow_payload, workflow_id)
    return f"Node was removed from the workflow. {res}"



#use edit sim and edit calibration instead..

# @tool("Remove Edge")
# def remove_edge(edge_id:str):
#     """
#     Removes an edge from the current workflow with a given id
#     You can find the id of the edge to be removed in the dictionary of the current workflow.
#     Edges represent connections between inputs and outputs of nodes and be used to do things like connect a dataset to a calibration, a model configuration to a simulate node, etc..
    
#     Parameters
#     ----------
#         edge_id (str) : The id of the edge to be deleted in the workflow dictionary
        
#     Returns
#     ----------
#         string indicating action success and the resulting new workflow or failure

#     """
#     workflow_id = WORKFLOW_ID
#     workflow_payload=get_workflow(workflow_id)
#     for i,edge in enumerate(workflow_payload['edges']):
#         if edge['id']==edge_id:
#             workflow_payload['edge'].pop(i)
#     res=modify_workflow(workflow_payload, workflow_id)
#     #to do: change connected status of i/o accordingly based on if they have a connection still..
#     return f"Edge was removed from the workflow. {res}"

# @tool("Add Edge")
# def add_edge(output_id:str,input_id:str):
#     """
#     Adds an edge between the output of one node, selected by its id, and the input of another node, selected by its id. Both ids can be found in the current workflow dictionary.
#     Edges represent connections between inputs and outputs of nodes and be used to do things like connect a dataset to a calibration, a model configuration to a simulate node, etc..
#     The valid edges are as follows:
#         A model node output to a simulate node input
#         A model node output to a calibrate input with type modelConfigId
#         A dataset node output to a calibrate input with type datasetId
    
#     Parameters
#     ----------
#         output_id (str) : The id of the output to be connected
#         input_id (str) : The id of the input to be connected
        
#     Returns
#     ----------
#         string indicating action success and the resulting new workflow or failure

#     """
#     #to do: check if edge to be created is valid and if not tell the LLM
#     workflow_id = WORKFLOW_ID
#     workflow_payload=get_workflow(workflow_id)
#     #get source id and target id from the workflow payload
#     target_id,source_id=None,None
#     target_type,source_type=None,None
#     output_dict,input_dict=None,None
#     for node in workflow_payload['nodes']:
#         for output in node['outputs']:
#             if output['id']==output_id:
#                 target_id=node['id']
#                 target_type=node["operationType"]
#                 output_dict=output
#         for inp in node['inputs']:
#             if inp['id']==input_id:
#                 source_id=node['id']
#                 source_type=node["operationType"]
#                 input_dict=inp
                
#     #check validity of edges given ids and types:
#     invalid_edge=False
#     if source_id==target_id:invalid_edge=True
#     if target_type!="SimulateCiemssOperation" or target_type!="CalibrationOperationCiemss":invalid_edge=True
#     if target_type=="SimulateCiemssOperation" and source_type!="ModelOperation":invalid_edge=True
#     if target_type=="CalibrationOperationCiemss":
#         if input_dict['type']!=output_dict['type']:invalid_edge=True
        
#     if invalid_edge:
#         return 'Requested edge is invalid, please check node and connection types and try again'
#     #update workflow
#     edge_payload, edge_uuid= generate_edge(workflow_id, source_id, target_id, output_id, input_id)
#     workflow_payload['edges'].append(edge_payload)
#     res=modify_workflow(workflow_payload, workflow_id)
#     #to do: change connected status of i/o accordingly
#     return f"Edge was added to the workflow. {res}"



#custom ask human
from typing import Callable, Optional

from langchain_core.pydantic_v1 import Field

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.tools.base import BaseTool
def _print_func(text: str) -> None:
    print("\n")
    print(text)
    
class HumanInputRun(BaseTool):
    """Tool that asks user for input."""

    name: str = "Ask User"
    description: str = """If the user asks you to perform an action but does not give all the inputs needed for using the tools required to perform those actions, ask the user clarifying questions. 
    If you are otherwise stuck, try to figure it out, but if you cannot, you can ask the user for help.
    Note that the user cannot see the current workflow state dictionary or any observations from any tools. 
    You should provide lots of context on the question you are asking to get a good response from the user."""
    prompt_func: Callable[[str], None] = Field(default_factory=lambda: _print_func)
    input_func: Callable = Field(default_factory=lambda: input)

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human input tool."""
        self.prompt_func(query)
        return self.input_func()

workflow_screen_tools=[add_model,search_models,lookup_model,lookup_model_config,edit_model_config_tool,
                       add_dataset,lookup_dataset,
                       add_simulation_tool,#edit_simulate_settings_tool,
                       add_calibrate_tool,#edit_calibrate_settings_tool,
                       HumanInputRun(),remove_node]#, add_edge,remove_edge,] #to use human input or nah? it is kind of annoying...
                        
                        #just replace all of this with editing the payload? or replace certain parts with add node and do if statements within?
                        #or add tool lookup?
                        #combine searches?
                        #combine lookups?

home_screen_tools=workflow_screen_tools+[create_workflow_tool,create_project_tool] #add ability to add workflows, projects from homescreen 
                    
