from io import BytesIO
from tempfile import TemporaryDirectory
from urllib.request import urlopen
from zipfile import ZipFile


def create_dependent_unused_artifacts(dir):
    """
    Create entities that are necessary to create other entities. This
    data does NOT come from upstream, it's just placeholder data
    to make sure stuff works
    """
    # TODO(five): Create person
    # TODO(five): Create petri framework


def create_placeholder_project(dir):
    """
    Create a project to store all the assets in
    """
    # TODO(five): Create sample project


def create_models(dir):
    """
    Create all the datasets listed in the directory
    """
    # TODO(five): Iterate over every directory
    # TODO(five): Upload paper
    # TODO(five): Upload model


def attach_concepts(dir):
    """
    Attach concepts to datasets, models, parameters, etc
    """
    # TODO(five): Attach a concept to each entity


def create_datasets(dir):
    """
    Create all the models listed in the directory
    """
    # TODO(five): Iterate over every directory
    # TODO(five): Upload dataset


def populate(url):
    """
    Populate TDS using data from the experiments repo
    """
    http_response = urlopen(url)
    with TemporaryDirectory() as temp_dir:
        # Download and extract experiments repo
        zipfile = ZipFile(BytesIO(http_response.read()))
        zipfile.extractall(str(temp_dir))

        # Populate data
        create_dependent_unused_artifacts(temp_dir)
        create_placeholder_project(temp_dir)
        create_models(temp_dir)
        create_datasets(temp_dir)
    print("Population is complete")
