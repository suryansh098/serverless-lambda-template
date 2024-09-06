# Serverless Lambda Template

This repository provides a **Serverless** template for building Lambda-based APIs with schema validation and structured controller logic. It includes utilities for handling event data, routing requests, and validating user inputs using Marshmallow.

## Table of Contents

- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Event Handling](#event-handling)
- [Validation](#validation)
- [Testing](#testing)
- [Contributing](#contributing)

## Project Structure

```
serverless-lambda-template/
│
├── cron_jobs/                    # Cron jobs handler files
├── mocks/                        # Mock files for testing
├── src/
│   ├── controllers/              # Lambda function controllers
│   ├── models/                   # Marshmallow schemas for request validation
│   └── routes/                   # API routes mapping
├── utils/                        # Utility functions (e.g., event processing)
│   └── event_utils.py            # Event processing utilities
├── handler.py                    # Main Lambda handler file
├── requirements.txt              # Python dependencies
├── tests/                        # Unit test files
└── README.md                     # Documentation file
```

## Installation

To use this template, clone the repository and install dependencies:

```bash
git clone https://github.com/suryansh098/serverless-lambda-template.git
cd serverless-lambda-template
pip install -r requirements.txt
```

## Usage

### Event Handling

The `handler.py` serves as the main entry point for processing Lambda events. It delegates requests to controllers based on routes defined in `src/routes.py`.

### Request Validation

`Marshmallow` is used for request validation. Input schemas are defined in `src/models/` and are used by the controllers to validate incoming requests.

### Routes

Routes are defined in `src/routes.py`, mapping resource paths to their respective controllers.

### Example: Login Flow

The `LoginController` handles user login logic and validation using the `LoginSchema`. The controller is responsible for validating the request body, authenticating the user, and returning appropriate responses.

## Testing

Unit tests are placed under the `tests/` directory. Each test class uses Python's `unittest` module. You can run the tests using:

```bash
python -m unittest discover -s test
```

## Contributing

If you'd like to contribute, please fork the repository and submit a pull request. Issues and bug reports are welcome!
