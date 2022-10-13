from hashlib import sha1
from json import dump, load
from pydbml import PyDBML
from omymodels import create_models
from os import makedirs
from os.path import exists, join
from pathlib import Path

from generation.fix import patch

INFO = 'info.json'
SCHEMAS = 'schema.py'


def get_dbml_version(dbml_path: str) -> str:
    dbml = PyDBML(Path(dbml_path))
    return dbml.project.note.text
    

def verify(version: str, generated_dir: str) -> bool:
    info_path = join(generated_dir, INFO)
    schema_path = join(generated_dir, SCHEMAS)
    if exists(info_path) and exists(schema_path):
        with open(schema_path, 'rb') as file:
            current_hash = sha1(file.read()).hexdigest()
        with open(info_path, 'r') as file:
            info = load(file)
        return info['version'] == version and info['hash'] == current_hash
    else:
        return False
 

def generate_validation(dbml_path: str, generated_dir: str) -> None:
    makedirs(generated_dir, exist_ok=True)

    dbml = PyDBML(Path(dbml_path))
    schemas = create_models(patch(dbml.sql), models_type='pydantic', dump_path=join(generated_dir, SCHEMAS))

    info = {
      'version': get_dbml_version(dbml_path),
      'hash': sha1(schemas['code'].encode()).hexdigest()
    }

    with open(join(generated_dir, INFO), 'w') as file:
        dump(info, file) 



