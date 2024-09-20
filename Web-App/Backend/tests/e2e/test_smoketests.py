import json
import pytest
from playwright.sync_api import Page
from support_scipts import load_users

@pytest.mark.usefixtures("app", "session")

def test_smoketest_dish(app, session, client, page: Page):
    print("Testing...")
    page.goto("/")
    page.get_by_role("button", name="Menu").click()
    page.wait_for_load_state("networkidle")
    page.get_by_role("link", name="Login").click()
    page.wait_for_load_state("networkidle")
    page.get_by_label("Username:").click()
    page.get_by_label("Username:").fill("admin@test.com")
    page.get_by_label("Password:").click()
    page.get_by_label("Password:").fill("admin_test")
    page.get_by_label("Password:").press("Enter")
    page.wait_for_load_state("networkidle")
