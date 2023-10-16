#! venv/bin/python
"""
Copy project CLI command.
"""
import argparse

from dev.tools.copy_project import CopyProject, CopyProjectFailed


def extract_args(cli_args) -> tuple:
    """
    Function extracts args from cli command.
    """
    return cli_args.id, cli_args.source, cli_args.destination, cli_args.model_config


# @TODO: Add STRATIFY = "Stratify" handling?

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
    parser.add_argument(
        "-c",
        "--model_config",
        help="Boolean to determine if the model configurations should be copied.",
        default="true",
    )
    args = parser.parse_args()
    project_id, source_url, destination_url, copy_configs = extract_args(args)

    if project_id and source_url and destination_url:
        print("Running copy project operation.")
        copy_class = CopyProject(
            pid=project_id,
            source=source_url,
            dest=destination_url,
            copy_configs=copy_configs == "true",
        )
        # Copy the project.
        copy_class.copy_project_obj()
        # Process the project assets. E.g. datasets, artifacts
        copy_class.process_assets()
        # Process the workflow objects.
        copy_class.process_workflows()
        # Validate the copy operation.
        try:
            copy_class.validate_copy()
            print("Copy project completed.")
            exit(0)
        except CopyProjectFailed as e_:
            print(e_.message)
    else:
        print("Missing required CLI option: project id, source url, or destination url")
    exit(1)
