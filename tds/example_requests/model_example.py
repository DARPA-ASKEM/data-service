import json

import requests

url = "http://localhost:8000/models"


payload = json.dumps(
    {
        "name": "Covid SIDARHTE",
        "description": "Petri net model to predict covid movement patters in a community",
        "content": json.dumps(
            {
                "S": [
                    {
                        "sname": "Susceptible",
                        "mira_ids": "[('identity', 'ido:0000514')]",
                        "mira_context": "[('property', 'ido:0000468')]",
                    },
                    {
                        "sname": "Infected",
                        "mira_ids": "[('identity', 'ido:0000511')]",
                        "mira_context": "[('property', 'ncit:C113725')]",
                    },
                    {
                        "sname": "Diagnosed",
                        "mira_ids": "[('identity', 'ido:0000511')]",
                        "mira_context": "[('property', 'ncit:C15220')]",
                    },
                    {
                        "sname": "Ailing",
                        "mira_ids": "[('identity', 'ido:0000573')]",
                        "mira_context": "[('property', 'ncit:C113725')]",
                    },
                    {
                        "sname": "Recognized",
                        "mira_ids": "[('identity', 'ido:0000511')]",
                        "mira_context": "[('property', 'ncit:C25587')]",
                    },
                    {
                        "sname": "Healed",
                        "mira_ids": "[]",
                        "mira_context": "[('property', 'ido:0000621')]",
                    },
                    {
                        "sname": "Threatened",
                        "mira_ids": "[('identity', 'ido:0000573')]",
                        "mira_context": "[('property', 'ncit:C15220')]",
                    },
                    {
                        "sname": "Extinct",
                        "mira_ids": "[('identity', 'ncit:C28554')]",
                        "mira_context": "[]",
                    },
                ],
                "T": [
                    {
                        "tname": "t1",
                        "template_type": "GroupedControlledConversion",
                        "parameter_name": "(('Susceptible', ('identity', 'ido:0000514'), ('property', 'ido:0000468')), ('Infected', ('identity', 'ido:0000511'), ('property', 'ncit:C113725')), (('Diagnosed', ('identity', 'ido:0000511'), ('property', 'ncit:C15220')), ('Ailing', ('identity', 'ido:0000573'), ('property', 'ncit:C113725')), ('Recognized', ('identity', 'ido:0000511'), ('property', 'ncit:C25587')), ('Infected', ('identity', 'ido:0000511'), ('property', 'ncit:C113725'))), 'GroupedControlledConversion', 'rate')",
                        "parameter_value": None,
                    },
                    {
                        "tname": "t2",
                        "template_type": "NaturalConversion",
                        "parameter_name": "epsilon",
                        "parameter_value": "0.171",
                    },
                    {
                        "tname": "t3",
                        "template_type": "NaturalConversion",
                        "parameter_name": "zeta",
                        "parameter_value": "0.125",
                    },
                    {
                        "tname": "t4",
                        "template_type": "NaturalConversion",
                        "parameter_name": "lambda",
                        "parameter_value": "0.034",
                    },
                    {
                        "tname": "t5",
                        "template_type": "NaturalConversion",
                        "parameter_name": "eta",
                        "parameter_value": "0.125",
                    },
                    {
                        "tname": "t6",
                        "template_type": "NaturalConversion",
                        "parameter_name": "rho",
                        "parameter_value": "0.034",
                    },
                    {
                        "tname": "t7",
                        "template_type": "NaturalConversion",
                        "parameter_name": "theta",
                        "parameter_value": "0.371",
                    },
                    {
                        "tname": "t8",
                        "template_type": "NaturalConversion",
                        "parameter_name": "kappa",
                        "parameter_value": "0.017",
                    },
                    {
                        "tname": "t9",
                        "template_type": "NaturalConversion",
                        "parameter_name": "mu",
                        "parameter_value": "0.017",
                    },
                    {
                        "tname": "t10",
                        "template_type": "NaturalConversion",
                        "parameter_name": "nu",
                        "parameter_value": "0.027",
                    },
                    {
                        "tname": "t11",
                        "template_type": "NaturalConversion",
                        "parameter_name": "xi",
                        "parameter_value": "0.017",
                    },
                    {
                        "tname": "t12",
                        "template_type": "NaturalConversion",
                        "parameter_name": "tau",
                        "parameter_value": "0.01",
                    },
                    {
                        "tname": "t13",
                        "template_type": "NaturalConversion",
                        "parameter_name": "sigma",
                        "parameter_value": "0.017",
                    },
                ],
                "I": [
                    {"is": 3, "it": 1},
                    {"is": 4, "it": 1},
                    {"is": 5, "it": 1},
                    {"is": 2, "it": 1},
                    {"is": 1, "it": 1},
                    {"is": 2, "it": 2},
                    {"is": 2, "it": 3},
                    {"is": 2, "it": 4},
                    {"is": 3, "it": 5},
                    {"is": 3, "it": 6},
                    {"is": 4, "it": 7},
                    {"is": 4, "it": 8},
                    {"is": 4, "it": 9},
                    {"is": 5, "it": 10},
                    {"is": 5, "it": 11},
                    {"is": 7, "it": 12},
                    {"is": 7, "it": 13},
                ],
                "O": [
                    {"os": 3, "ot": 1},
                    {"os": 4, "ot": 1},
                    {"os": 5, "ot": 1},
                    {"os": 2, "ot": 1},
                    {"os": 2, "ot": 1},
                    {"os": 3, "ot": 2},
                    {"os": 4, "ot": 3},
                    {"os": 6, "ot": 4},
                    {"os": 5, "ot": 5},
                    {"os": 6, "ot": 6},
                    {"os": 5, "ot": 7},
                    {"os": 6, "ot": 8},
                    {"os": 7, "ot": 9},
                    {"os": 7, "ot": 10},
                    {"os": 6, "ot": 11},
                    {"os": 8, "ot": 12},
                    {"os": 6, "ot": 13},
                ],
            }
        ),
        "parameters": {
            "alpha": "int",
            "beta": "int",
            "gamma": "int",
            "delta": "int",
            "epsilon": "int",
            "theta": "int",
            "zeta": "int",
            "eta": "int",
            "mu": "int",
            "nu": "int",
            "tau": "int",
            "kappa": "int",
            "rho": "int",
            "sigma": "int",
            "xi": "int",
            "Event_trigger_Fig3b": "int",
            "Event_trigger_Fig3d": "int",
            "Event_trigger_Fig4b": "int",
            "Event_trigger_Fig4d": "int",
            "epsilon_modifier": "int",
            "alpha_modifier": "int",
            "ModelValue_16": "int",
            "ModelValue_17": "int",
            "ModelValue_18": "int",
            "ModelValue_19": "int",
            "ModelValue_21": "int",
            "ModelValue_20": "int",
            "Italy": "int",
            "XXlambdaXX": "int",
        },
    }
)
headers = {"Content-Type": "application/json"}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
