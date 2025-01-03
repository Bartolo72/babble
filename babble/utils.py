from dotenv import dotenv_values
from typing import Dict

from .exceptions import EnvVariableNotFound


def get_env_variable(variable_name: str) -> str:
    """
    Retrieves the value of an environment variable from the .env file.

    Args:
        variable_name (str): The name of the environment variable to retrieve.

    Raises:
        EnvVariableNotFound: If the environment variable is not found in the .env file.

    Returns:
        str: The value of the environment variable.

    """
    config: Dict[str, str] = dotenv_values(".env")
    var: str = config.get(variable_name, "")
    if not var:
        raise EnvVariableNotFound(variable_name)
    return var
