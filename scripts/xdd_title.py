import glob
import json

import requests

url = "https://xdd.wisc.edu/api/articles?docid="
xdd = "5ef119afa58f1dfd5209bd33"
folders = glob.glob("experiments*/thin-thread-examples/biomodels/BIOMD*/")


def get_xdd_title(xdd_id, url="https://xdd.wisc.edu/api/articles?docid="):
    response = requests.request("GET", url + xdd_id)

    resp_json = response.json()
    return resp_json["success"]["data"][0]["title"]


mapping = {}
for folder in folders:
    with open(folder + "document_xdd_gddid.txt", "r") as f:
        gddid = f.read()
        mapping[gddid] = get_xdd_title(gddid)

with open("scripts/xdd_mapping.json", "w") as f:
    f.write(json.dumps(mapping))
print(mapping)
