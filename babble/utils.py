from dotenv import dotenv_values
from typing import Dict

from .exceptions import EnvVariableNotFound


def get_env_variable(variable_name: str) -> str:
    config: Dict[str, str] = dotenv_values(".env")
    var: str = config.get(variable_name, "")
    if not var:
        raise EnvVariableNotFound(variable_name)
    return var
