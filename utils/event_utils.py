"""
Event Utility Module

This module provides the `EventUtils` class, which offers helper methods to
extract and manage data from an event object in an API-driven application.
It handles common tasks such as retrieving the body, request type, origin,
resource path, and query parameters from the event payload. These utilities 
are particularly useful in scenarios involving AWS Lambda, API Gateway, or 
any other serverless environment where events are triggered via HTTP requests.

Usage:
    event_utils = EventUtils(event)
    body = event_utils.get_body()
    resource = event_utils.get_resource()
    request_type = event_utils.get_request_type()
    query_params = event_utils.get_query_params()
"""

import json
import logging


class EventUtils:
    """
    A utility class for extracting data from event objects in API-driven
    applications.

    Attributes:
        event (dict): The event object containing request details.

    Methods:
        get_body(): Returns the parsed body of the event, or raises an error if empty.
        get_resource(): Retrieves the request path (resource) from the event.
        get_request_origin(): Fetches the request origin from the headers.
        get_request_type(): Retrieves the HTTP method used for the request.
        get_query_params(): Fetches query parameters from the event.
    """

    def __init__(self, event) -> None:
        """
        Initializes the EventUtils class with the given event.

        Args:
            event (dict): The event object received by the API handler.
        """
        self.event = event

    def get_body(self) -> dict:
        """
        Parses and returns the body of the event as a dictionary.

        Logs an info message if the body is found, and raises a ValueError if the body is empty.

        Returns:
            dict: Parsed body of the event.

        Raises:
            ValueError: If the body is empty or not provided.
        """
        body = self.event.get("body", {})
        logging.info("Received body - %s", body)
        if body:
            return json.loads(body)
        logging.error("Body was empty")
        raise ValueError("Body was empty")

    def get_resource(self):
        """
        Retrieves the request path (resource) from the event.

        Returns:
            str or int: The request path if present, otherwise 404.
        """
        if self.event.get("path", None):
            return self.event.get("path")
        logging.error("Resource not found in the request")
        return 404

    def get_request_origin(self):
        """
        Retrieves the origin of the request from the headers.

        Returns:
            str: The origin of the request if present in the headers.
        """
        request_headers = self.event.get("headers", {})
        request_headers = {key.lower(): value for key, value in request_headers.items()}

        if request_headers:
            return request_headers.get("origin")

    def get_request_type(self) -> str:
        """
        Retrieves the HTTP method used in the request.

        Logs an error if the HTTP method is not found and raises a ValueError.

        Returns:
            str: The HTTP method of the request.

        Raises:
            ValueError: If the HTTP method is not found in the event.
        """
        if self.event.get("httpMethod", None):
            return self.event.get("httpMethod")
        logging.error("Request type not found in the request")
        raise ValueError("Request type not found in the request")

    def get_query_params(self) -> dict:
        """
        Fetches the query parameters from the event.

        Returns:
            dict: The query parameters.

        Raises:
            ValueError: If query parameters are not found in the event.
        """
        if self.event.get("queryStringParameters", None):
            return self.event.get("queryStringParameters")
        logging.error("Query parameters not found in the request")
        raise ValueError("Query parameters not found in the request")
