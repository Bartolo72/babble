from typing import Dict, Any


class EnvVariableNotFound(Exception):
    def __init__(self: "EnvVariableNotFound", variable_name: str) -> None:
        message: str = (
            f"Please check that you have .env file in your environment and variable {variable_name} is defined"
        )
        super().__init__(message)


class InvalidResponse(Exception):
    def __init__(
        self: "InvalidResponse",
        code: int,
        reason: str,
        url: str,
        body: Dict[str, Any] = {},
    ) -> None:
        message: str = f"Response Error! URL: {url}.\nCode: {code}.\nReason: {reason}."
        if body:
            message += f"\nBody: {body}"
        super().__init__(message)


class TriggerInfeasible(Exception):
    correct_pos = ["start", "mid", "end"]
    correct_size = 60

    def __init__(self, size, pos):
        self.size = size
        self.pos = pos
        self.message = (
            f"Cannot apply trigger (size: {self.size}, pos: "
            f"{self.pos}). Size should be in (0, "
            f"{self.correct_size}] and pos should be in "
            f"{self.correct_pos}"
        )
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"
