"""
Model configurations to fill out Swagger doc examples.
"""
model_config = {
    "header": {
        "name": "A Test Model",
        "schema": "https://raw.githubusercontent.com/DARPA-ASKEM/Model-Representations/petrinet_v0.2/petrinet/petrinet_schema.json",  # pylint: disable=line-too-long
        "description": "Test Model Post from Swagger.",
        "model_version": "1.0",
    },
    "model": {
        "states": [
            {
                "id": "S",
                "name": "S",
                "grounding": {
                    "identifiers": {"ncbitaxon": "9606"},
                    "context": {},
                },
            },
            {
                "id": "V",
                "name": "V",
                "grounding": {
                    "identifiers": {"ncbitaxon": "9606"},
                    "context": {},
                },
            },
        ],
        "transitions": [
            {
                "id": "t1",
                "input": ["S"],
                "output": [],
                "properties": {
                    "name": "t1",
                    "rate": {
                        "expression": "S/l_e",
                        "expression_mathml": "<apply><divide/><ci>S</ci><ci>l_e</ci></apply>",  # pylint: disable=line-too-long
                    },
                },
            },
            {
                "id": "t2",
                "input": ["V"],
                "output": [],
                "properties": {
                    "name": "t2",
                    "rate": {
                        "expression": "V/l_e",
                        "expression_mathml": "<apply><divide/><ci>V</ci><ci>l_e</ci></apply>",  # pylint: disable=line-too-long
                    },
                },
            },
        ],
        "parameters": [{"id": "l_e", "value": 50.0}],
    },
}
