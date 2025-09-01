import os

import pytest

from bootcamp_lib.lambda_middleware import http_request, UserRoles


def build_auth_body(profile):
    return {
        "body": "",
        "requestContext": {
            "authorizer": {"claims": {"profile": profile, "name": "Test user"}}
        }
    }


def teardown_function():
    os.environ.pop("USER_PROFILE", None)


@http_request
def lambda_to_test(request, _context):
    return {
        "field": {"Content": "value"}
    }


@pytest.mark.order(-1)
def test_profile_access_permitted(aws_credentials):
    os.environ["USER_PROFILE"] = "{},{}".format(UserRoles.AGENT, UserRoles.ADMIN)
    response = lambda_to_test(build_auth_body(UserRoles.AGENT), None)
    assert response["statusCode"] == 200


@pytest.mark.order(-1)
def test_profile_access_denied():
    os.environ["USER_PROFILE"] = UserRoles.ADMIN
    response = lambda_to_test(build_auth_body(UserRoles.AGENT), None)

    assert response["statusCode"] == 403
    assert response["body"] == '{"error": "Forbidden"}'


@pytest.mark.order(-1)
def test_profile_access_no_lambda_profile():
    response = lambda_to_test(build_auth_body(UserRoles.AGENT), None)
    assert response["statusCode"] == 200
