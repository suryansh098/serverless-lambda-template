"""
TestLogin Module

This module contains unit tests for the login functionality. It creates a mock event
and context and calls the `handle` function to simulate login behavior. The tests ensure
the correct response is returned for valid login credentials.

Classes:
    - EventContext: Creates a mock event containing the request details for the login process.
    - Context: Represents a mock AWS Lambda context object for testing.
    - TestLogin: Contains unit tests for the login functionality.

Usage:
    Use `TestLogin` to execute tests on the login handler and ensure proper behavior.
"""

from unittest import TestCase
import os
import sys
import json
import warnings
from handler import handle

# Adjusting the import path to include the parent directory for the handler module
test_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, test_path + "/../")


def ignore_warnings(test_func):
    """Decorator to filter out the warnings in tests
    Args:
        test_func (func): any test function
    """

    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            test_func(self, *args, **kwargs)

    return do_test


USER_ID = 1000


class EventContext:
    """
    EventContext

    This class simulates the event object passed to the AWS Lambda handler function.
    It represents a login request event.

    Attributes:
        event (dict): The event object simulating the login request.
    """

    def __init__(self):
        """
        Initializes the EventContext with a predefined POST login request.

        The request contains:
            - Path: "/user/login/"
            - HTTP method: POST
            - Headers: Mock origin header
            - Request context: Simulated user ID
            - Body: Encoded JSON object with email and password
        """
        self.event = {
            "resource": "/user/login/",
            "path": "/user/login/",
            "httpMethod": "POST",
            "headers": {"origin": "https://google.com/"},
            "multiValueHeaders": None,
            "requestContext": {"authorizer": {"user_id": USER_ID}},
            "pathParameters": None,
            "queryStringParameters": None,
            "body": json.dumps(
                {"email": "test@gmail.com", "password": "strongpassword"}
            ),
        }


class Context:
    """
    Context

    Simulates the AWS Lambda context object for testing purposes.

    Attributes:
        aws_request_id (str): The unique request ID for the Lambda function invocation.
    """

    def __init__(self, aws_request_id) -> None:
        """
        Initializes the Context with an AWS request ID.

        Args:
            aws_request_id (str): The AWS request ID passed during the Lambda invocation.
        """
        self.aws_request_id = aws_request_id


class TestLogin(TestCase):
    """
    TestLogin

    Contains unit tests for the login functionality. Tests that valid credentials
    return a successful response.

    Methods:
        test_login: Tests the login functionality by invoking the Lambda handler
                    with a mock event and context.
    """

    @ignore_warnings
    def test_login(self):
        """
        Tests the login process using the mock event and context.

        Ensures that the Lambda handler returns a 200 status code for valid login credentials.
        """
        event = EventContext().event
        response = handle(event, Context("from_integration_testcase"))
        self.assertEqual(response["statusCode"], 200)
