import playwright
import pytest
from playwright.async_api import Page
from playwright.sync_api import expect

from tests.conftest import load_users, perform_login


@pytest.mark.usefixtures("session")
def test_suggestion_accept(page: Page, load_users, delete_all_dishes, delete_all_meal_plans):
    users = load_users
    kantinenmitarbeiter_user = next(user for user in users if user.get("role") == "kantinenmitarbeiter")
    perform_login(page, kantinenmitarbeiter_user["email"], kantinenmitarbeiter_user["password"])
    page.get_by_role("button", name="Menu").click()
    page.get_by_role("link", name="Gerichte hinzufügen").click()
    page.wait_for_load_state('networkidle')
    expect(page).to_have_url("/#/createDish")
    page.get_by_label("Name*").click()
    page.get_by_label("Name*").fill("NewDish")
    page.get_by_label("Preis*").click()
    page.get_by_label("Preis*").fill("5")
    page.get_by_placeholder("Inhaltsstoff").click()
    page.get_by_placeholder("Inhaltsstoff").fill("Test1")
    page.get_by_role("button", name="Inhaltsstoff hinzufügen").click()
    page.get_by_placeholder("Inhaltsstoff 2").click()
    page.get_by_placeholder("Inhaltsstoff 2").fill("Test2")
    page.get_by_role("button", name="Inhaltsstoff hinzufügen").click()
    page.get_by_placeholder("Inhaltsstoff 3").click()
    page.get_by_placeholder("Inhaltsstoff 3").fill("Test3")
    page.get_by_label("Ernährungsklasse*").select_option("Vegetarisch")
    page.get_by_label("Mahlzeitentyp*").select_option("Abendessen")
    page.get_by_label("Allergien").check()
    page.get_by_role("button", name="Speichern").click()
    expect(page.get_by_text("Gericht erfolgreich erstellt")).to_be_visible()
    page.get_by_role("button", name="Menu").click()
    page.get_by_role("link", name="Essensplans Anlegen").click()
    page.get_by_label("Gerichtsart auswählen").locator("svg").click()
    page.get_by_role("option", name="Abendessen").click()
    page.get_by_label("Gericht auswählen").locator("svg").click()
    expect(page.locator("#mat-option-5")).to_contain_text("NewDish")
