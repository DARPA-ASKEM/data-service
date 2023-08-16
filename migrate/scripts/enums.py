from typing import Iterator

import sqlalchemy as sa
from alembic import op
from sqlalchemy import Column

provenance_type = sa.Enum(
    "Concept",
    "Dataset",
    "Model",
    "ModelConfiguration",
    "Project",
    "Publication",
    "Simulation",
    name="provenancetype",
)
resource_type = sa.Enum(
    "datasets",
    "models",
    "model_configurations",
    "publications",
    "simulations",
    "workflows",
    name="resourcetype",
)
extracted_type = sa.Enum("equation", "figure", "table", name="extractedtype")
taggable_type = sa.Enum(
    "datasets",
    "models",
    "projects",
    "publications",
    "qualifiers",
    "simulation_parameters",
    "model_configurations",
    "simulations",
    "workflows",
    name="taggabletype",
)
role = sa.Enum("author", "contributor", "maintainer", "other", name="role")
ontological_field = sa.Enum("obj", "unit", name="ontologicalfield")
relation_type = sa.Enum(
    "BEGINS_AT",
    "CITES",
    "COMBINED_FROM",
    "CONTAINS",
    "COPIED_FROM",
    "DECOMPOSED_FROM",
    "DERIVED_FROM",
    "EDITED_FROM",
    "EQUIVALENT_OF",
    "EXTRACTED_FROM",
    "GENERATED_BY",
    "GLUED_FROM",
    "IS_CONCEPT_OF",
    "PARAMETER_OF",
    "REINTERPRETS",
    "STRATIFIED_FROM",
    "USES",
    name="relationtype",
)

value_type = sa.Enum("binary", "bool", "float", "int", "str", name="valuetype")


def update_enum(name: str, enum_obj: sa.Enum, cols: dict, enum_entities: list) -> None:
    for key in cols:
        print(key)
        if type(cols[key]) is list:
            for col_key in cols[key]:
                alter_enum_col(table_name=key, col_name=col_key, enum_obj=enum_obj)
        else:
            alter_enum_col(table_name=key, col_name=cols[key], enum_obj=enum_obj)
    drop_enums([enum_obj])
    new_enum = sa.Enum(*enum_entities, name=name)
    for key_1 in cols:
        if type(cols[key_1]) is list:
            for col_key_1 in cols[key_1]:
                convert_enum_col(
                    table_name=key_1, col_name=col_key_1, new_enum=new_enum
                )
        else:
            convert_enum_col(table_name=key_1, col_name=cols[key_1], new_enum=new_enum)


def alter_enum_col(table_name: str, col_name: str, enum_obj: sa.Enum):
    with op.batch_alter_table(table_name) as batch_op:
        batch_op.alter_column(
            col_name,
            existing_type=enum_obj,
            type=sa.String(),
        )


def convert_enum_col(table_name: str, col_name: str, new_enum: sa.Enum):
    with op.batch_alter_table(table_name) as batch_op:
        new_col = f"{col_name}_copy"
        batch_op.add_column(column=Column(name=new_col, type_=new_enum))
    with op.batch_alter_table(table_name) as batch_op_2:
        batch_op_2.execute(f"UPDATE {table_name} SET {new_col} = {col_name};")
        batch_op_2.drop_column(col_name)
        batch_op_2.alter_column(new_col, new_column_name=col_name)


# Alembic 1.9.4 does not support dropping enums on downgrade on autogen. So,
# ... we separate enum declarations from upgrade.
def drop_enums(enums: Iterator[sa.Enum]):
    """
    Drop a list of enums
    """
    for enum in enums:
        enum.drop(op.get_bind(), checkfirst=False)
