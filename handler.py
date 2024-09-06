"""
Handler Module

This module provides the main event handler function that processes incoming API events,
extracts relevant request data (like resource and request type), and routes the request 
to the appropriate controller for execution. The controller is dynamically loaded based 
on predefined routes, and if no matching controller is found, a 404 response is returned.

It leverages utility functions to parse the event and manage request types and paths.

Usage:
    The `handle(event, context)` function should be invoked as part of an AWS Lambda function,
    or similar serverless architecture, to process incoming requests and route them appropriately.
"""

import re
import json
import logging
import importlib
from utils.event_utils import EventUtils
from src.routes import ROUTES

logging.getLogger().setLevel(logging.INFO)


def get_controller(resource: str, request_type: str):
    """
    Retrieves the appropriate controller class for the provided resource and request type.

    Args:
        resource (str): The API resource (e.g., endpoint path) to match against the routes.
        request_type (str): The HTTP method (e.g., GET, POST) used for the request.

    Returns:
        str or None: The name of the controller class if a match is found, otherwise None.
    """
    for key, value in ROUTES.items():
        if re.match(key, resource):
            return value[request_type]
    return None


def handle(event: dict, context) -> dict:
    """
    Main handler function that processes an event and routes it to the appropriate controller.

    Args:
        event (dict): The event object received by the API handler, typically containing request data.
        context (object): The context object provided by AWS Lambda, containing runtime information.

    Returns:
        dict: The response object, containing a status code and body.
    """
    logging.info("Entered with event - %s", event)

    # Initialize the EventUtils to help extract useful event data
    event_utils = EventUtils(event)

    # Extract resource path and log it
    resource = event_utils.get_resource()
    logging.info("Resource: %s", resource)

    # Extract the HTTP method and log it
    request_type = event_utils.get_request_type()
    logging.info("Request-type: %s", request_type)

    # Retrieve the AWS request ID from the context object
    pid = context.aws_request_id

    # Determine the correct controller for the given resource and request type
    controller = get_controller(resource=resource, request_type=request_type)
    logging.info("Controller - %s", controller)

    response = {}

    if controller:
        # Dynamically import and instantiate the controller class
        module = importlib.import_module(
            "src.controllers." + controller.lower() + "_controller"
        )
        class_ = getattr(module, controller + "Controller")
        instance = class_(event, pid)

        # Execute the controller and store the response
        response = instance.execute()

    else:
        # Handle case where no matching resource is found
        logging.info("No resource matched: provided resource is: %s", resource)
        response = {
            "statusCode": 404,
            "body": json.dumps({"message": "Resource not found!"}),
        }

    # Log the final response
    logging.info("Response: %s", response)

    return response
