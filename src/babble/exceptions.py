from typing import Literal, Dict, Any


class EnvVariableNotFound(Exception):
    def __init__(self: "EnvVariableNotFound", variable_name: str) -> None:            
        message: str = f"Please check that you have .env file in your environment and variable {variable_name} is defined"
        super().__init__(message)
            


class InvalidResponse(Exception):
    def __init__(self: "InvalidResponse", code: int, reason: str, url: str, body: Dict[str, Any] = {}) -> None:
        message: str = f"Response Error! URL: {url}.\nCode: {code}.\nReason: {reason}."
        if body:
            message += f"\nBody: {body}"
        super().__init__(message)