from dataclasses import fields
from typing import get_args


def generate_frontend_schema(dataclass_type, exclude: list[str] | None = None):
    global_schema = {}

    if not exclude:
        exclude = []

    for f in fields(dataclass_type):
        field_name = f.name
        field_value = getattr(dataclass_type, field_name)
        if field_name in exclude:
            continue
        field_type = f.type

        args = get_args(field_type)

        field_type = args[0]
        field_schema = args[1]
        field_schema["value"] = field_value
        global_schema[field_name] = field_schema

    return global_schema
