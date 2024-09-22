import pytest
from playwright.sync_api import expect, Page

from tests.conftest import load_users, perform_login, perform_logout


@pytest.mark.usefixtures("session")
def test_suggestion_accept(page: Page, load_users, delete_all_dish_suggestions, delete_all_dishes):
    users = load_users
    kantinenmitarbeiter_user = next(user for user in users if user.get("role") == "kantinenmitarbeiter")
    hungernder_user = next(user for user in users if user.get("role") == "hungernder")

    perform_login(page, hungernder_user["email"], hungernder_user["password"])
    page.get_by_role("button", name="Menu").click()
    page.get_by_role("link", name="Menüvorschlag").click()
    expect(page).to_have_url("/#/createSuggestion")
    page.get_by_placeholder("Name des Gerichts").click()
    page.get_by_placeholder("Name des Gerichts").fill("TestVorschlag")
    page.get_by_placeholder("Beschreibe dein Gericht dem").click()
    page.get_by_placeholder("Beschreibe dein Gericht dem").fill("Testbeschreibung")
    page.get_by_placeholder("Inhaltsstoff").click()
    page.get_by_placeholder("Inhaltsstoff").fill("Test1")
    page.get_by_role("button", name="Inhaltsstoff hinzufügen").click()
    page.get_by_placeholder("Inhaltsstoff 2").click()
    page.get_by_placeholder("Inhaltsstoff 2").fill("Test2")
    page.get_by_role("button", name="Vorschlag einreichen").click()
    expect(page.get_by_text("Gerichtsvorschlag erfolgreich")).to_be_visible()
    perform_logout(page)

    perform_login(page, kantinenmitarbeiter_user["email"], kantinenmitarbeiter_user["password"])

    page.get_by_role("button", name="Menu").click()
    page.get_by_role("link", name="Menüvorschläge bearbeiten").click()
    expect(page).to_have_url("/#/suggestionReview")
    page.get_by_label("Name*").click()
    page.get_by_label("Name*").fill("TestVorschlag edited")
    page.get_by_label("Preis in €*").click()
    page.get_by_label("Preis in €*").fill("05")
    page.get_by_label("Ernährungsklasse*").select_option("Vegetarisch")
    page.get_by_label("Mahlzeitentyp*").select_option("Mittagessen")
    page.get_by_label("Allergien").check()
    page.get_by_role("button", name="Akzeptieren").first.click()

    page.get_by_role("button", name="Menu").click()
    page.get_by_role("link", name="Essensplans Anlegen").click()
    page.wait_for_load_state('networkidle')
    page.locator("div").filter(has_text="Gericht auswählen").nth(4).click()
    page.get_by_label("Gericht auswählen").locator("span").click()
    page.get_by_label("Gericht auswählen").locator("svg").click()
    page.get_by_label("Gericht auswählen").locator("path").click()
    page.locator("div").filter(has_text="Gericht auswählen").nth(4).click()
    page.get_by_text("Gericht auswählenGericht ausw").click()
    page.locator("div").filter(has_text="Gericht auswählen").nth(4).click()
    page.get_by_label("Gericht auswählen").locator("span").click()
    page.locator("div").filter(has_text="Gerichtsart auswählen").nth(4).click()
    page.get_by_role("option", name="Mittagessen").click()
    page.locator("div").filter(has_text="Gericht auswählen").nth(4).click()
    expect(page.get_by_role("option", name="TestVorschlag edited")).to_be_visible()


def test_suggestion_decline(page: Page, load_users, delete_all_dish_suggestions, delete_all_dishes):
    users = load_users
    kantinenmitarbeiter_user = next(user for user in users if user.get("role") == "kantinenmitarbeiter")

    hungernder_user = next(user for user in users if user.get("role") == "hungernder")

    perform_login(page, hungernder_user["email"], hungernder_user["password"])

    page.get_by_role("button", name="Menu").click()
    page.get_by_role("link", name="Menüvorschlag").click()
    expect(page).to_have_url("/#/createSuggestion")
    page.get_by_placeholder("Name des Gerichts").click()
    page.get_by_placeholder("Name des Gerichts").fill("TestVorschlag")
    page.get_by_placeholder("Beschreibe dein Gericht dem").click()
    page.get_by_placeholder("Beschreibe dein Gericht dem").fill("Testbeschreibung")
    page.get_by_placeholder("Inhaltsstoff").click()
    page.get_by_placeholder("Inhaltsstoff").fill("Test1")
    page.get_by_role("button", name="Inhaltsstoff hinzufügen").click()
    page.get_by_placeholder("Inhaltsstoff 2").click()
    page.get_by_placeholder("Inhaltsstoff 2").fill("Test2")
    page.get_by_role("button", name="Vorschlag einreichen").click()
    expect(page.get_by_text("Gerichtsvorschlag erfolgreich")).to_be_visible()
    perform_logout(page)

    perform_login(page, kantinenmitarbeiter_user["email"], kantinenmitarbeiter_user["password"])

    page.get_by_role("button", name="Menu").click()
    page.get_by_role("link", name="Menüvorschläge bearbeiten").click()
    expect(page).to_have_url("/#/suggestionReview")
    expect(page.get_by_label("Name*")).to_have_value("TestVorschlag")
    page.get_by_label("Name*").click()
    page.get_by_label("Name*").fill("TestVorschlag edited")
    page.get_by_label("Preis in €*").click()
    page.get_by_label("Preis in €*").fill("05")
    page.get_by_label("Ernährungsklasse*").select_option("Vegetarisch")
    page.get_by_label("Mahlzeitentyp*").select_option("Mittagessen")
    page.get_by_label("Allergien").check()
    page.get_by_role("button", name="Ablehnen").first.click()
    expect(page.get_by_text("No Suggestions found")).to_be_visible()
