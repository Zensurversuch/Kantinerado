import json
import os
import pytest
from playwright.sync_api import Page


@pytest.fixture(scope="session")
def load_users():
    file_path = os.path.join(os.path.dirname(__file__), 'user.json')
    with open(file_path) as f:
        return json.load(f)

