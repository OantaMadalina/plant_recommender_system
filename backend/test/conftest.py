import os
import sys
import logging

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

os.environ["environment"] = "bootcampengine_test_"
os.environ["BOOTCAMP_BUCKET"] = "test"
os.environ["APPDYNAMICS_DISABLE_AGENT"] = "true"


def pytest_configure(config):
    logging.getLogger("flake8").setLevel(logging.ERROR)
