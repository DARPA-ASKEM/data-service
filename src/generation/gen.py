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
ORM = 'orm.py'


def get_dbml_version(dbml_path: str) -> str:
    dbml = PyDBML(Path(dbml_path))
    return dbml.project.note.text
    

def verify(version: str, generated_dir: str) -> bool:
    info_path = join(generated_dir, INFO)
    schema_path = join(generated_dir, SCHEMAS)
    orm_path = join(generated_dir, ORM)
    if exists(info_path) and exists(schema_path):
        with open(orm_path, 'rb') as file:
            orm_hash = sha1(file.read()).hexdigest()
        with open(schema_path, 'rb') as file:
            schema_hash = sha1(file.read()).hexdigest()
        with open(info_path, 'r') as file:
            info = load(file)
        return info['version'] == version and info['schema_hash'] == schema_hash and info['orm_hash'] == orm_hash
    else:
        return False
 

def generate_validation(dbml_path: str, generated_dir: str) -> None:
    makedirs(generated_dir, exist_ok=True)

    dbml = PyDBML(Path(dbml_path))
    schemas = create_models(patch(dbml.sql), models_type='pydantic', dump_path=join(generated_dir, SCHEMAS))
    orm = create_models(patch(dbml.sql), models_type='sqlalchemy', dump_path=join(generated_dir, ORM))

    info = {
      'version': get_dbml_version(dbml_path),
      'schema_hash': sha1(schemas['code'].encode()).hexdigest(),
      'orm_hash': sha1(orm['code'].encode()).hexdigest()
    }

    with open(join(generated_dir, INFO), 'w') as file:
        dump(info, file) 



