from json import dump, load
from pydbml import PyDBML
from omymodels import create_models
from os import makedirs
from os.path import exists, join
from pathlib import Path

from generation.fix import patch

INFO = 'info.json'

def get_dbml_version(dbml_path: str) -> str:
    dbml = PyDBML(Path(dbml_path))
    return dbml.project.note.text
    

def get_schema_version(generated_dir: str) -> str:
    info_path = join(generated_dir, INFO)
    if exists(info_path):
        with open(info_path, 'r') as file:
            info = load(file)  
            return info['version']
    else:
        return ''
 

def generate_validation(dbml_path: str, generated_dir: str) -> None:
    makedirs(generated_dir, exist_ok=True)

    dbml = PyDBML(Path(dbml_path))
    create_models(patch(dbml.sql), models_type='pydantic', dump_path=join(generated_dir, 'schema.py'))

    info = {
      'version': get_dbml_version(dbml_path),
    }

    with open(join(generated_dir, INFO), 'w') as file:
        dump(info, file) 



