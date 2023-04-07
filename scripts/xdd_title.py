import glob
import json

import requests

url = "https://xdd.wisc.edu/api/articles?docid="
xdd = "5ef119afa58f1dfd5209bd33"
folders = sorted(
    glob.glob("experiments*/thin-thread-examples/mira_v1/biomodels/BIOMD*/")
    + glob.glob("experiments*/thin-thread-examples/starter-kit/*/")
)


def get_xdd_title(xdd_id, url="https://xdd.wisc.edu/api/articles?docid="):
    print(xdd_id)
    response = requests.request("GET", url + xdd_id)

    resp_json = response.json()
    if "success" in resp_json:
        return resp_json["success"]["data"][0]["title"]
    else:
        return None


mapping = {}
for folder in folders:
    with open(folder + "document_xdd_gddid.txt", "r") as f:
        gddid = f.read()
        mapping[gddid] = get_xdd_title(gddid)

# how to add an xdd id manually.
mapping["636cbb6a74bed2df5c1bc9f7"] = get_xdd_title("636cbb6a74bed2df5c1bc9f7")

with open("scripts/xdd_mapping.json", "w") as f:
    f.write(json.dumps(mapping))
print(mapping)
