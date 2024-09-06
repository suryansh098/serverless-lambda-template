"""
Login Controller Module

This module handles the login process for incoming requests. It utilizes `LoginSchema` 
to validate the login request data and performs basic authentication. If validation fails, 
appropriate error responses are returned.

Classes:
    - LoginController: Manages the validation and authentication of login requests.

Usage:
    Instantiate the `LoginController` with the event data and process ID (pid).
    Call the `execute` method to process the login request and return the appropriate response.
"""

import json
import logging
from marshmallow import ValidationError
from utils.event_utils import EventUtils
from src.models.login_schema import LoginSchema


class LoginController:
    """
    LoginController

    Handles the login request by validating the request body and authenticating the user.

    Attributes:
        event (dict): The event data containing the login request.
        pid (str): The process ID associated with the current request.
        body (dict): The parsed body of the event, containing login credentials.

    Methods:
        _authenticate: Authenticates the user based on the provided email and password.
        execute: Validates the request body, attempts to authenticate the user, and returns a response.
    """

    def __init__(self, event, pid) -> None:
        """
        Initializes the LoginController with the event and process ID.

        Args:
            event (dict): The event containing the login request.
            pid (str): The process ID associated with the current request.

        Initializes:
            body (dict): Parsed request body data from the event.
        """
        event_utils = EventUtils(event)
        self.body = event_utils.get_body()
        self.pid = pid

    def _authenticate(self):
        """
        Private method to authenticate the login credentials.

        Checks if the provided email and password match the hardcoded credentials.
        For now, the password is hardcoded as "strongpassword".

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        email = self.body["email"]
        password = self.body["password"]

        if email and password == "strongpassword":
            return True
        return False

    def execute(self):
        """
        Main method to execute the login process.

        This method validates the incoming request body using the `LoginSchema`.
        If validation passes, it attempts to authenticate the user. Depending on
        the outcome of the authentication, it returns a success or failure response.

        Returns:
            dict: A dictionary containing the HTTP status code and response body.
        """
        try:
            schema = LoginSchema()
            schema.load(self.body)
        except ValidationError as ve:
            logging.error(ve)
            missing_keys = str(list(ve.normalized_messages().keys()))
            return {
                "statusCode": 422,
                "body": json.dumps({"message": f"{missing_keys} are missing!"}),
            }

        if self._authenticate():
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Login successful!"}),
            }

        return {
            "statusCode": 403,
            "body": json.dumps({"message": "Either email or password is incorrect!"}),
        }
