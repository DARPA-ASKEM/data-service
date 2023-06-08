"""
TDS Dataset Response module.
"""
from tds.modules.dataset.model import Dataset


def dataset_response(es_list):
    """
    Function forms a dataset list response.
    """
    return [Dataset(**hit["_source"]) for hit in es_list]
