import pytest
from babble.utils import get_env_variable
from babble.exceptions import EnvVariableNotFound


def test_get_env():
    with pytest.raises(EnvVariableNotFound):
        get_env_variable(variable_name="babble_env_test")
