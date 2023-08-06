from typing import Callable
from ..pydantic_model import PydanticModel, Field


def _key_parent(key: str):
    parts = None
    for delim in ("_", "."):
        if delim in key:
            parts == key.split(delim, 1)
            break
    if parts is None:
        parts = [key, ""]
    return parts[0], parts[1]


class _VarLine(PydanticModel):
    key: str = Field("")
    parent: str = Field("")
    value: str = Field("")
    is_varline: bool = Field(False)


def __varline(line: str):
    if "=" in line:
        kv = line.split("=", 1)
        key = kv[0].strip()
        value = kv[1].lstrip()
        key, parent = _key_parent(key=key)
        result = _VarLine(key=key, value=value, parent=parent, is_varline=True)
    else:
        result = _VarLine()
    return result


def varline(__line: str, postinit_varline: Callable[[dict], dict] = None):
    result = __varline(__line).dict()
    if postinit_varline is not None:
        result = postinit_varline(result)
    return result
