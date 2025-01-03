from typing import Dict, Any


class EnvVariableNotFound(Exception):
    """
    Exception raised when a required environment variable is not found in the .env file.
    """

    def __init__(self: "EnvVariableNotFound", variable_name: str) -> None:
        """
        Initializes the exception with a message indicating the missing environment variable.

        Args:
            variable_name (str): The name of the environment variable that is missing.
        """
        message: str = (
            f"Please check that you have .env file in your environment and variable {variable_name} is defined"
        )
        super().__init__(message)


class InvalidResponse(Exception):
    """
    Exception raised when a response from an external service is invalid or contains errors.
    """

    def __init__(
        self: "InvalidResponse",
        code: int,
        reason: str,
        url: str,
        body: Dict[str, Any] = {},
    ) -> None:
        """
        Initializes the exception with a message containing response error details.

        Args:
            code (int): The HTTP status code from the response.
            reason (str): A brief explanation of why the response was invalid.
            url (str): The URL that was requested.
            body (Dict[str, Any], optional): The body of the response (default is an empty dictionary).
        """
        message: str = f"Response Error! URL: {url}.\nCode: {code}.\nReason: {reason}."
        if body:
            message += f"\nBody: {body}"
        super().__init__(message)


class TriggerInfeasible(Exception):
    """
    Exception raised when an operation cannot be performed due to invalid trigger parameters.
    """

    correct_pos = ["start", "mid", "end"]
    correct_size = 60

    def __init__(self, size, pos):
        """
        Initializes the exception with the invalid trigger size and position.

        Args:
            size (int): The invalid size of the trigger.
            pos (str): The invalid position of the trigger (must be one of 'start', 'mid', 'end').
        """
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
        """
        Returns the string representation of the exception message.

        Returns:
            str: The exception message describing the invalid trigger.
        """
        return f"{self.message}"
