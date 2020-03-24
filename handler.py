import json
import logging
import os
from urllib.parse import parse_qs

import boto3

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)


def hello(event, context):
    log_stream(event, context)

    name = "World"
    content_type = event.get("multiValueHeaders", dict()).get("content-type")
    input_body = event.get("body")

    if input_body:
        if "application/x-www-form-urlencoded" in content_type:
            name = "".join(parse_qs(input_body).get("name", name))
        if "application/json" in content_type:
            name = json.loads(input_body).get("name", name)
    else:
        name = event.get("name", name)

    body = {
        "message": f"Hello {name}!",
        "input": event,
    }

    response = {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }

    return response


def whoami(event, context):
    log_stream(event, context)
    body = {
        "message": boto3.client("sts").get_caller_identity(),
        "input": event,
    }
    response = {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": body,
    }

    return response


def log_stream(event, context):
    _LOGGER.debug("ENVIRONMENT VARIABLES: %s", os.environ)

    _LOGGER.info("Function name: %s", context.function_name)
    _LOGGER.info("Function version: %s", context.function_version)
    _LOGGER.info("Log stream name: %s", context.log_stream_name)
    _LOGGER.info("Log group name: %s", context.log_group_name)
    _LOGGER.info("Request ID: %s", context.aws_request_id)
    _LOGGER.info("Mem. limits(MB): %s", context.memory_limit_in_mb)
