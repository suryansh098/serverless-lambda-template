"""
Schema Module

This module defines validation schemas for input data using Marshmallow, a powerful object 
serialization/deserialization and validation library. The `LoginSchema` class provides a 
schema for validating login requests, ensuring that required fields like email and password 
are correctly formatted and provided.
"""

from marshmallow import Schema, fields


class LoginSchema(Schema):
    """
    LoginSchema

    This schema validates the structure of login data, specifically checking for a valid email
    and password string. Both fields are required.

    Fields:
        - email (str): A valid email address that is required for login.
        - password (str): A password string that is required for login.

    Usage:
        schema = LoginSchema()
        result = schema.load(data)  # Validates the incoming login data.
    """

    email = fields.Email(
        required=True, error_messages={"required": "Email is required"}
    )
    password = fields.String(
        required=True, error_messages={"required": "Password is required"}
    )
