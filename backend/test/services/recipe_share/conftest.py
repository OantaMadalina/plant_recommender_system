import os

import pytest


@pytest.fixture(scope="module")
def aws_credentials():
    os.environ["environment"] = "mcprengine_test_"
    os.environ["aws_account_id"] = "123456789012"
    os.environ["AWS_REGION"] = "eu-west-1"
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-1"
    os.environ["MCPR_BUCKET"] = "test"
