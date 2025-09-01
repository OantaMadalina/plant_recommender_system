from dataclasses import dataclass, is_dataclass, asdict, field
import base64
import json
from http import HTTPStatus
import os
import gzip

import appdynamics
from aws_lambda_powertools.middleware_factory import lambda_handler_decorator

from bootcamp_lib.logger import Logger


class HttpException(Exception):
    HTTP_STATUS: HTTPStatus


class BadRequestException(HttpException):
    HTTP_STATUS = HTTPStatus.BAD_REQUEST


class NotFoundException(HttpException):
    HTTP_STATUS = HTTPStatus.NOT_FOUND


class ConflictException(HttpException):
    HTTP_STATUS = HTTPStatus.CONFLICT


class InternalServerErrorException(HttpException):
    HTTP_STATUS = HTTPStatus.INTERNAL_SERVER_ERROR


class WarningException(Exception):
    """Used for generating a warning instead of an ERROR log entry"""


class ErrorException(Exception):
    """Used for generating an ERROR log entry without stack trace"""


class InfoException(Exception):
    """Used for generating an info entry instead of an ERROR log entry"""


class UserRoles:
    ADMIN = "APP-UK-CavendishAdmin"
    SUPPLY_CHAIN = "APP-UK-CavendishSupplyChain"
    TERMINALS = "APP-UK-CavendishTerminals"
    AGENT_MANAGER = "APP-UK-CavendishAgentManager"
    AGENT = "APP-UK-CavendishAgent"
    WAREHOUSE_OPS = "APP-UK-CavendishWarehouseOps"
    BACK_OFFICE = "APP-UK-CavendishBackOffice"


@dataclass
class HttpRequestData:
    body: str = ""
    dictBody: dict = field(default_factory=dict)
    headers: dict = field(default_factory=dict)
    queryParams: dict = field(default_factory=dict)
    pathParams: dict = field(default_factory=dict)
    username: str = ""
    userProfile: str = ""

    @property
    def maskCustomerInfo(self) -> bool:
        return (self.userProfile not in
                [UserRoles.AGENT_MANAGER, UserRoles.SUPPLY_CHAIN, UserRoles.ADMIN,
                 UserRoles.BACK_OFFICE])


@dataclass
class AttachmentFileResponse:
    body: str = ""
    filename: str = ""


def validate_body(body: dict, validation: dict, path: list):
    """
    Recursively validates a dictionary using a validation scheme. It supports lists and objects.
    """
    for field_name, spec in validation.items():
        field_path = path + [field_name]
        field_value = body.get(field_name)

        type_mapping = {
            "boolean": bool,
            "integer": int
        }
        spec_type = spec.get("type")
        spec_type_cls = type_mapping.get(spec_type)

        if spec.get("required") and field_value in ("", None):
            full_field_name = ".".join(field_path)
            raise BadRequestException(f"Body field '{full_field_name}' is required")
        elif spec_type_cls and not isinstance(field_value, spec_type_cls):
            full_field_name = ".".join(field_path)
            raise BadRequestException(f"Body field '{full_field_name}' must be {spec_type}")

        if field_value not in ("", None):
            if "properties" in spec:
                validate_body(body[field_name], spec["properties"], field_path)
            elif "items" in spec:
                if not isinstance(body[field_name], list):
                    full_field_name = ".".join(field_path)
                    raise BadRequestException(f"Body field '{full_field_name}' must be a list")
                for index, item in enumerate(body[field_name]):
                    if "properties" in spec["items"]:
                        field_path = path + [f"{field_name}[{index}]"]
                        validate_body(item, spec["items"]["properties"], field_path)


def process_headers(headers: dict) -> dict:
    Logger().structure_logs(append=True, X_TransactionID=headers.get("X-TransactionID"))
    Logger().structure_logs(append=True, X_Source=headers.get("X-Source"))

    response_headers = {
        "Access-Control-Allow-Origin": "*"
    }

    if "X-TransactionID" in headers:
        response_headers["X-TransactionID"] = headers.get("X-TransactionID")

    if "X-Source" in headers:
        response_headers["X-Source"] = "Cavendish"

    if "Date" in headers:
        response_headers["Date"] = headers.get("Date")

    return response_headers


@lambda_handler_decorator
def lambda_logger(
        handler, event, context, logged_fields: dict = {}, log_input: bool = False,
        log_response: bool = False, persistent_log_fields: list = [], reraise: bool = True):
    if context:
        Logger().set_correlation_id(context.aws_request_id)

    if persistent_log_fields:
        Logger().structure_logs(append=True, **{field: None for field in persistent_log_fields})

    if logged_fields:
        event_fields = {}
        for log_field, event_field in logged_fields.items():
            val = event
            for elem in event_field.split("."):
                val = val.get(elem)
                if val is None:
                    break

            event_fields[log_field] = val

        Logger().structure_logs(append=True, **event_fields)

    Logger().info("Event: %s", event if log_input else "", extra={"type": "START"})

    @appdynamics.tracer
    def execute_lambda(event, context):
        try:
            response = handler(event, context)
            Logger().info("Response: %s", response if log_response else "", extra={"type": "END"})
            return response
        except WarningException as exc:
            Logger().warning(str(exc), exc_info=exc)
            if reraise:
                raise
            else:
                appdynamics.report_error("FailedLambda", "Failed lambda")
        except ErrorException as exc:
            Logger().error(str(exc))
            if reraise:
                raise
            else:
                appdynamics.report_error("FailedLambda", "Failed lambda")
        except InfoException as exc:
            Logger().info(str(exc), extra={"type": "END"})
            if reraise:
                raise
        except Exception:
            Logger().exception("Lambda function exception", extra={"type": "FAIL"})
            if reraise:
                raise
            else:
                appdynamics.report_error("FailedLambda", "Failed lambda")

    return execute_lambda(event, context)


@lambda_handler_decorator
def http_request(
        handler, event, context, request_type: str = "GET", validation: dict = {},
        content_type: str = "application/json", persistent_log_fields: list = [],
        wrap_root_tag: bool = False, log_response: bool = True, disable_request: bool = False,
        raw_response: bool = False, gzip_compressed: bool = False, json_load_method=json.loads):
    """
    HTTP request middleware which allows validation, dataclasses as lambda function response.

    Args:
    - handler: The lambda function handler.
    - event: The event object containing the request details.
    - context: The context object for the lambda function.
    - request_type: The type of the HTTP request.
    - validation: Validation rules for the request body.
    - content_type: The content type of the request.
    - persistent_log_fields:
        A list of fields which are included in the log root structure.
    - wrap_root_tag:
        A boolean indicating whether to wrap the request body with a root tag for XML validation.
    - log_response: A boolean indicating whether to log the response (default: True).
    - disable_request: A boolean indicating whether to disable the lambda invocation.
    - raw_response:
        A boolean indicating whether to return the response as it's returned from the lambda.
    - gzip_compressed: A boolean indicating whether to compress the response using gzip.
    - json_load_method: The method to use for loading JSON data.

    Returns:
    - response_obj: A dictionary containing the HTTP response.
    """

    response_obj = {
        "headers": process_headers(event.get("headers", {}))
    }
    if gzip_compressed:
        response_obj["isBase64Encoded"] = True

    if context:
        Logger().set_correlation_id(context.aws_request_id)

    request_body = event.get("body")
    # authorizer = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})

    # Add root tag for the XML validation - root tag is required
    if wrap_root_tag:
        request_body = "<root>\n" + request_body.replace(
            '<?xml version="1.0" encoding="UTF-8"?>', '').strip() + "\n</root>"

    # user_roles = [r for r in UserRoles.__dict__.values() if isinstance(r, str)]
    # profile = next((r for r in user_roles if r in authorizer.get("profile", "")), None)

    request = HttpRequestData(
        body=request_body,
        headers=event.get("headers", {}),
        queryParams=event.get("queryStringParameters") or {},
        pathParams=event.get("pathParameters") or {},
        # username=authorizer.get("name", "Unknown user"),
        # userProfile=profile or UserRoles.AGENT
    )

    if disable_request and "Postman" not in event["headers"]["User-Agent"]:
        Logger().info(
            "Endpoint disabled - QueryStringParameters: %s\nPathParameters: %s\nBody: %s",
            request.queryParams, request.pathParams, event.get("body", ""), extra={"type": "START"})

        response_obj["headers"]["Content-type"] = "application/json"
        response_obj["statusCode"] = HTTPStatus.FORBIDDEN.value
        response_obj["body"] = json.dumps({"error": "Endpoint disabled"})
        return response_obj

    log_response_extra = {"type": "END"}
    if persistent_log_fields:
        Logger().structure_logs(append=True, **{field: None for field in persistent_log_fields})

    Logger().info(
        "QueryStringParameters: %s\nPathParameters: %s\nBody: %s",
        request.queryParams, request.pathParams, event.get("body", ""), extra={"type": "START"})

    # limit function invocation to specified roles
    allowed_roles = [
        role for role in map(str.strip, os.getenv("USER_PROFILE", "").split(",")) if role]

    if allowed_roles and request.userProfile not in allowed_roles:
        response_obj["headers"]["Content-type"] = "application/json"
        response_obj["statusCode"] = HTTPStatus.FORBIDDEN.value
        response_obj["body"] = json.dumps({"error": "Forbidden"})
        Logger().warning(
            "Unauthorized access for user '%s' with role '%s'",
            request.username, request.userProfile)

        return response_obj

    @appdynamics.tracer
    def execute_lambda(request, context):
        nonlocal content_type

        try:
            # validate parameters
            if request_type in ("POST", "PUT"):
                if content_type == "application/json":
                    body = json_load_method(event["body"])
                    validate_body(body, validation, [])
                    request.dictBody = body

            if content_type == "application/xml":
                http_status, response = handler(request, context)
                status = http_status.value
            else:
                response = handler(request, context)
                if isinstance(response, tuple):
                    http_status, response = response
                    status = http_status.value
                else:
                    status = 200

            if isinstance(response, AttachmentFileResponse):
                response_obj["headers"]["Content-Disposition"] = "attachment; filename={}".format(
                    response.filename
                )
                response_obj["isBase64Encoded"] = True
                response = base64.b64encode(response.body)
            elif is_dataclass(response):
                response = asdict(response)
            elif isinstance(response, list):
                for index in range(len(response)):
                    if is_dataclass(response[index]):
                        response[index] = asdict(response[index])

            if status >= 500:
                log_status = "FAIL"
                appdynamics.report_error("RequestFailed", "Failed request")

            elif status >= 400:
                log_status = "REJECT"
                appdynamics.report_error("RequestRejected", "Rejected request")
            else:
                log_status = "ACCEPT"

        except HttpException as ex:
            status = ex.HTTP_STATUS.value
            if content_type == "application/xml":
                response = str(ex)
            else:
                content_type = "application/json"
                response = {
                    "error": str(ex)
                }

            log_status = "REJECT"
            appdynamics.report_error("RequestRejected", "Rejected request")

        except Exception:
            Logger().exception("Unhandled request in http_request middleware")
            status = HTTPStatus.INTERNAL_SERVER_ERROR.value
            content_type = "application/json"
            response = {
                "error": HTTPStatus.INTERNAL_SERVER_ERROR.phrase
            }

            log_status = "FAIL"
            log_response_extra.update({"type": "FAIL", "status": "REJECT"})
            appdynamics.report_error("RequestFailed", "Failed request")

        return status, response, content_type, log_status

    status, response, content_type, log_status = execute_lambda(request, context)

    if raw_response and isinstance(response, dict) and "statusCode" in response:
        response_obj = {
            "headers": process_headers(event.get("headers", {}))
        }
        response["headers"].update(response_obj["headers"])
        Logger().info({"response": response})
        return response

    response_obj["headers"]["Content-type"] = content_type
    if gzip_compressed:
        response_obj["headers"]["Content-Encoding"] = "gzip"
    response_obj["statusCode"] = status

    if content_type == "application/json":
        response_obj["body"] = json.dumps(response)
    else:
        response_obj["body"] = response

    if gzip_compressed:
        response_obj["body"] = base64.b64encode(gzip.compress(bytes(response_obj["body"], "utf-8")))

    log_response_extra["statusCode"] = status
    log_response_extra["status"] = log_status

    Logger().info(
        "Response: %s", response_obj["body"] if log_response else "", extra=log_response_extra)

    return response_obj
