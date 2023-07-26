import json
import uuid

import requests


def post_to_destination(url: str, body: dict | None):
    """
    Function runs post request to url.
    """
    print(f"Posting to {url}")
    obj_create = requests.post(
        url=url, data=json.dumps(body) if body else None, timeout=120
    )
    return obj_create.json()


def put_to_destination(url: str, body: dict):
    """
    Function runs put request to url.
    """
    print(f"Putting to {url}")
    obj_create = requests.put(url=url, data=json.dumps(body), timeout=120)
    return obj_create.json()


def scrub_obj(obj: dict):
    """
    Function scrubs system items from object before copying.
    """
    new_obj = {}
    for key in obj.keys():
        if key in ["id", "timestamp"]:
            continue
        new_obj[key] = obj[key]

    return new_obj


class CopyProjectFailed(Exception):
    def __init__(self, message="Copy project failed for reasons."):
        super().__init__()
        self.message = message


class CopyProject:
    """
    Class handles copying project between environments.
    """

    asset_url = "{host}/projects/{project_id}/assets/{asset_type}/{asset_id}"
    download_url = "{host}/{asset_type}/{asset_id}/download-url"
    upload_url = "{host}/{asset_type}/{asset_id}/upload-url"
    resource_url = "{host}/{resource_uri}/{entity_id}"
    post_url = "{host}/{resource}"
    source_project = None
    source_project_assets = None
    source_project_workflows = None
    destination_project_id = None
    id_mapper = {
        "datasets": {},
        "models": {},
        "model_configurations": {},
        "publications": {},
        "simulations": {},
        "artifacts": {},
    }
    simulation_types = [
        "CalibrationOperationJulia",
        "CalibrationOperationCiemss",
        "SimulateJuliaOperation",
        "CalibrateEnsembleCiemms",
        "SimulateEnsembleCiemms",
        "SimulateCiemssOperation",
    ]

    def __init__(self, pid: int, source: str, dest: str):
        self.project_id = pid
        self.source_url = source
        self.destination_url = dest

    def copy_project_obj(self):
        """
        Function copies base project to destination.
        """
        self._fetch_project()
        new_project = scrub_obj(self.source_project)
        post_url = self.post_url.format(host=self.destination_url, resource="projects")
        response = post_to_destination(url=post_url, body=new_project)
        new_project["id"] = response["id"]
        self.destination_project_id = response["id"]

    def process_assets(self):
        """
        Function processes project assets.
        """

        for key in self.source_project_assets:
            if len(self.source_project_assets[key]) and key != "workflows":
                resource_uri = key if key != "publications" else "external/publications"
                for asset in self.source_project_assets[key]:
                    asset_url = self.resource_url.format(
                        host=self.source_url, resource_uri=resource_uri, entity_id=asset
                    )
                    asset_fetch = requests.get(url=asset_url, timeout=120)
                    asset_json = asset_fetch.json()
                    asset_resp = self._post_asset(
                        asset=asset_json, asset_type=resource_uri
                    )
                    asset_id = asset_resp["id"]
                    self.id_mapper[key][asset] = asset_id
                    asset_url = self.asset_url.format(
                        host=self.destination_url,
                        project_id=self.destination_project_id,
                        asset_type=key,
                        asset_id=asset_id,
                    )
                    post_to_destination(url=asset_url, body=None)
                    if key in ["datasets", "artifacts"]:
                        files = (
                            asset_json["result_files"]
                            if key == "simulation"
                            else asset_json["file_names"]
                        )
                        source_download_url = self.download_url.format(
                            host=self.source_url,
                            asset_type=key,
                            asset_id=asset,
                        )
                        destination_upload_url = self.upload_url.format(
                            host=self.destination_url,
                            asset_type=key,
                            asset_id=asset_id,
                        )
                        for file in files:
                            download_url_request = requests.get(
                                url=source_download_url,
                                params={"filename": file},
                                timeout=120,
                            )
                            download_response = download_url_request.json()
                            download_url = download_response["url"]
                            download_file = requests.get(url=download_url, timeout=120)

                            upload_url_request = requests.get(
                                url=destination_upload_url,
                                params={"filename": file},
                                timeout=120,
                            )
                            upload_url = upload_url_request.json()

                            requests.put(
                                url=upload_url["url"],
                                files={f"{file}": download_file.content},
                                timeout=120,
                            )

    def process_workflows(self):
        """
        Function processes workflows.
        """
        # with open(
        #     "/Users/hephaestus/Sites/Jataware/data-service/mapper.json", "r"
        # ) as f:
        #     self.id_mapper = json.loads(f.read())

        for source_workflow_id in self.source_project_workflows:
            workflow_json = self._fetch_from_source(
                resource_uri="workflows", resource_id=source_workflow_id
            )
            workflow_nodes = workflow_json.pop("nodes")
            workflow_edges = workflow_json.pop("edges")
            workflow_post_url = self.post_url.format(
                host=self.destination_url, resource="workflows"
            )
            workflow_post = post_to_destination(
                url=workflow_post_url, body=scrub_obj(workflow_json)
            )
            workflow_id = workflow_post["id"]
            new_nodes = self._process_workflow_nodes(
                nodes=workflow_nodes, workflow_id=workflow_id
            )
            new_edges = self._process_workflow_edges(
                edges=workflow_edges, workflow_id=workflow_id
            )
            workflow_json["id"] = workflow_id
            workflow_json["nodes"] = new_nodes
            workflow_json["edges"] = new_edges
            workflow_put_url = self.post_url.format(
                host=self.destination_url, resource=f"workflows/{workflow_id}"
            )
            put_to_destination(url=workflow_put_url, body=workflow_json)

    def validate_copy(self):
        """
        Method does a simple validation based on entity array lengths in project.
        """
        new_project = self._fetch_from_destination(
            resource_uri="projects", resource_id=self.destination_project_id
        )
        failed_resources = []
        for entity in self.source_project.keys():
            if len(new_project[entity]) == len(self.source_project[entity]):
                print(f"{entity} length is correct.")
            else:
                failed_resources.append(entity)

        if len(failed_resources) > 0:
            msg = ",".join(failed_resources)
            raise CopyProjectFailed(message=f"{msg} lengths do not match.")

    def _fetch_project(self):
        """
        Function fetches project from origin.
        """

        self.source_project = self._fetch_from_source(
            resource_uri="projects", resource_id=self.project_id
        )
        self.source_project_assets = self.source_project.pop("assets")
        self.source_project_workflows = self.source_project_assets["workflows"]

    def _process_workflow_nodes(self, nodes: list, workflow_id: str):
        """
        Method is a delegator that processes workflow nodes.
        """
        updated_nodes = []
        models = [x for x in nodes if x["operationType"] == "ModelOperation"]
        self._process_workflow_models(models)
        for node in nodes:
            node_obj = node
            if "workflowId" in node_obj:
                node_obj["workflowId"] = workflow_id
            op = node["operationType"]
            if op in self.simulation_types:
                node_obj = self._process_simulation_node(node_obj)
            elif op == "Dataset":
                node_obj["state"]["datasetId"] = self.id_mapper["datasets"][
                    node["state"]["datasetId"]
                ]
            elif op == "ModelOperation":
                node_obj["state"]["modelId"] = self.id_mapper["models"][
                    node["state"]["modelId"]
                ]
            else:
                print(f"{op} is not currently supported.")
            updated_nodes.append(node_obj)
        return updated_nodes

    def _process_workflow_edges(self, edges: list, workflow_id: str):
        """
        Method processes the workflow edges.
        """
        updated_edges = []
        for edge in edges:
            new_edge = edge
            new_edge["workflowId"] = workflow_id
            updated_edges.append(new_edge)

        return updated_edges

    def _process_workflow_models(self, models: list):
        """
        Method processes the workflow model objects to extract configurations.
        """
        for model in models:
            new_model_id = self.id_mapper["models"][model["state"]["modelId"]]

            if len(model["inputs"]):
                print("WE HAVE INPUTS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                for model_input in model["inputs"]:
                    print(model_input)
            if len(model["outputs"]):
                for model_output in model["outputs"]:
                    if model_output["type"] == "modelConfigId":
                        for val in model_output["value"]:
                            self._process_model_config(
                                model_config_id=val, new_model_id=new_model_id
                            )

    def _process_model_config(self, model_config_id: str, new_model_id: str):
        """
        Method process a model node from the source project workflow.
        """
        # If we already have an id mapped, continue.
        if model_config_id in self.id_mapper["model_configurations"].keys():
            return
        model_config_post_url = self.post_url.format(
            host=self.destination_url, resource="model_configurations"
        )
        model_config = self._fetch_from_source(
            resource_uri="model_configurations", resource_id=model_config_id
        )
        model_config = scrub_obj(model_config)
        model_config["model_id"] = new_model_id
        model_config_post = post_to_destination(
            url=model_config_post_url, body=model_config
        )
        self.id_mapper["model_configurations"][model_config_id] = model_config_post[
            "id"
        ]

    def _process_simulation_node(self, simulation_node: dict):
        """
        Method processes a simulation object.
        """

        if (
            self.id_mapper["simulations"]
            and simulation_node in self.id_mapper["simulations"].keys()
        ):
            return
        new_simulation_node = simulation_node
        if len(new_simulation_node["inputs"]):
            new_inputs = []
            for sim_input in simulation_node["inputs"]:
                new_input = sim_input
                if new_input["type"] == "modelConfigId":
                    new_vals = []
                    # If value param is not in the input, just continue because it is only an operational object.
                    if "value" not in new_input.keys():
                        continue
                    for val in new_input["value"]:
                        new_vals.append(self.id_mapper["model_configurations"][val])
                    new_input["value"] = new_vals
                    new_inputs.append(new_input)
            new_simulation_node["inputs"] = new_inputs

        if len(new_simulation_node["outputs"]):
            new_outputs = []
            for sim_output in simulation_node["outputs"]:
                new_vals = []
                new_output = sim_output
                if new_output["type"] == "simOutput":
                    for val in new_output["value"]:
                        sim_obj = self._process_simulation(simulation_id=val)
                        new_vals.append(sim_obj["id"])
                    new_output["value"] = new_vals
                new_outputs.append(new_output)

            new_simulation_node["outputs"] = new_outputs
        return new_simulation_node

    def _process_simulation(self, simulation_id: str):
        """
        Method copies a simulation from the source to the destination.
        """
        sim_obj = self._fetch_from_source(
            resource_uri="simulations", resource_id=simulation_id
        )
        sim_id_parts = sim_obj["id"].split("-")
        sim_obj = scrub_obj(sim_obj)
        prefix = sim_id_parts.pop(0)
        sim_id_parts.pop(-1)
        suffix = "copied"
        sim_uuid = f"{prefix}-{uuid.uuid4()}-{suffix}"
        sim_obj["id"] = sim_uuid
        if sim_obj["execution_payload"]:
            sim_exec_payload = sim_obj["execution_payload"]
            if (
                sim_exec_payload
                and "model_config_id" in sim_exec_payload
                and sim_exec_payload["model_config_id"]
                in self.id_mapper["model_configurations"].keys()
            ):
                sim_obj["execution_payload"]["model_config_id"] = self.id_mapper[
                    "model_configurations"
                ][sim_exec_payload["model_config_id"]]
        # Blank out result files for now - Todd R. July 26, 2023.
        sim_obj["result_files"] = []
        sim_url = self.post_url.format(
            host=self.destination_url, resource="simulations"
        )
        post_to_destination(url=sim_url, body=sim_obj)
        return sim_obj

    def _post_asset(self, asset, asset_type):
        """
        Function posts asset to destination.
        """
        post_url = self.post_url.format(host=self.destination_url, resource=asset_type)

        return post_to_destination(url=post_url, body=scrub_obj(asset))

    def _fetch_from_source(self, resource_uri: str, resource_id):
        """
        Method fetches resource from source system.
        """
        return self._fetch_from_url(
            host=self.source_url, resource_uri=resource_uri, resource_id=resource_id
        )

    def _fetch_from_destination(self, resource_uri: str, resource_id):
        """
        Method fetches resource from source system.
        """
        return self._fetch_from_url(
            host=self.destination_url,
            resource_uri=resource_uri,
            resource_id=resource_id,
        )

    def _fetch_from_url(self, host: str, resource_uri: str, resource_id):
        """
        Method fetches resource from url.
        """
        entity_url = self.resource_url.format(
            host=host, resource_uri=resource_uri, entity_id=resource_id
        )
        entity_fetch = requests.get(entity_url, timeout=120)
        fetch_json = entity_fetch.json()
        return fetch_json
