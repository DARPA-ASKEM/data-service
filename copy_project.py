#! venv/bin/python
"""
Copy project CLI command.
"""
import argparse
import json

import requests


def extract_args(cli_args) -> tuple:
    """
    Function extracts args from cli command.
    """
    return cli_args.id, cli_args.source, cli_args.destination


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


def post_to_destination(url: str, body: dict | None):
    """
    Function runs post request to url.
    """
    print(f"Posting to {url}")
    obj_create = requests.post(
        url=url, data=json.dumps(body) if body else None, timeout=120
    )
    return obj_create.json()


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
    destination_project_id = None

    def __init__(self, pid: int, source: str, dest: str):
        self.project_id = pid
        self.source_url = source
        self.destination_url = dest

    def fetch_project(self):
        """
        Function fetches project from origin.
        """
        fetch_url = self.resource_url.format(
            host=self.source_url, resource_uri="projects", entity_id=self.project_id
        )
        print(f"Fetching project from: {fetch_url}")
        project_fetch = requests.get(url=fetch_url, timeout=120)
        self.source_project = project_fetch.json()
        self.source_project_assets = self.source_project.pop("assets")

    def copy_project_obj(self):
        """
        Function copies base project to destination.
        """
        new_project = scrub_obj(self.source_project)
        post_url = self.post_url.format(host=self.destination_url, resource="projects")
        response = post_to_destination(url=post_url, body=new_project)
        self.destination_project_id = response["id"]

    def process_assets(self):
        """
        Function processes project assets.
        """
        for key in self.source_project_assets:
            if len(self.source_project_assets[key]):
                resource_uri = key if key != "publications" else "external/publications"
                for asset in self.source_project_assets[key]:
                    asset_url = self.resource_url.format(
                        host=self.source_url, resource_uri=resource_uri, entity_id=asset
                    )
                    asset_fetch = requests.get(url=asset_url, timeout=120)
                    asset_json = asset_fetch.json()
                    asset_resp = self.post_asset(
                        asset=asset_json, asset_type=resource_uri
                    )
                    asset_id = asset_resp["id"]
                    asset_url = self.asset_url.format(
                        host=self.destination_url,
                        project_id=self.destination_project_id,
                        asset_type=key,
                        asset_id=asset_id,
                    )
                    asset_relationship = post_to_destination(url=asset_url, body=None)
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

                            upload_file = requests.put(
                                url=upload_url["url"],
                                files={f"{file}": download_file.content},
                                timeout=120,
                            )

    def post_asset(self, asset, asset_type):
        """
        Function posts asset to destination.
        """
        post_url = self.post_url.format(host=self.destination_url, resource=asset_type)

        return post_to_destination(url=post_url, body=scrub_obj(asset))


if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--id", help="The id for the project in the source system."
    )
    parser.add_argument(
        "-s",
        "--source",
        help="The source URL to copy the project from including protocol and port (if needed). "
        "E.g. http://localhost:8001",
    )
    parser.add_argument(
        "-d",
        "--destination",
        help="The destination URL to copy the project to including protocol and port "
        "(if needed). E.g. http://localhost:8001",
    )
    args = parser.parse_args()
    project_id, source_url, destination_url = extract_args(args)

    if project_id and source_url and destination_url:
        print("Running copy project operation.")
        copy_class = CopyProject(
            pid=project_id, source=source_url, dest=destination_url
        )
        # Get the project.
        copy_class.fetch_project()
        copy_class.copy_project_obj()
        copy_class.process_assets()
    else:
        print("Missing required CLI option: porject id, source url, or destination url")
