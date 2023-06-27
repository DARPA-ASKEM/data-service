"""
TDS Provenance Utilities.
"""
import json


def return_graph_validations():
    """
    read in graph relation file
    """
    with open("graph_relations.json", "r", encoding="utf-8") as file:
        validation = json.load(file)
    return validation


def validate_relationship(left, right, relation_type):
    """
    validate a relationship for provenance
    """
    validations = return_graph_validations()
    relationship_allowed_types = validations[relation_type]
    for relation in relationship_allowed_types:
        if left == relation[0] and right == relation[1]:
            return True
    return False
