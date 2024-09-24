import pytest
from playwright.sync_api import Page, expect
from tests.conftest import load_users, perform_login, perform_logout


@pytest.mark.usefixtures("session")
def test_register_kantinenmitarbeiter(page: Page, load_users, delete_all_users):
    users = load_users
    admin_user = next(user for user in users if user.get("role") == "admin")
    new_kantinenmitarbeiter = next(user for user in users if user.get("role") == "new_kantinenmitarbeiter")
    perform_login(page, admin_user["email"], admin_user["password"])

    page.get_by_role("button", name="Menu").click()
    page.get_by_role("link", name="Benutzer Registrieren").click()
    page.get_by_label("Nachname*").click()
    page.get_by_label("Nachname*").fill(new_kantinenmitarbeiter["lastName"])
    page.get_by_label("Vorname*").click()
    page.get_by_label("Vorname*").fill(new_kantinenmitarbeiter["firstName"])
    page.get_by_label("E-Mail*").click()
    page.get_by_label("E-Mail*").fill(new_kantinenmitarbeiter["email"])
    page.get_by_label("E-Mail*").click()
    page.get_by_label("Rolle*").select_option("kantinenmitarbeiter")
    page.get_by_label("Passwort*", exact=True).click()
    page.get_by_label("Passwort*", exact=True).fill(new_kantinenmitarbeiter["password"])
    page.get_by_label("Bestätige Passwort*").click()
    page.get_by_label("Bestätige Passwort*").fill(new_kantinenmitarbeiter["password"])
    page.get_by_role("button", name="Registrieren").click()
    perform_logout(page)
    perform_login(page, new_kantinenmitarbeiter["email"], new_kantinenmitarbeiter["password"])
    expect(page).to_have_url("/#/")
    page.get_by_role("button", name="Menu").click()
    expect(page.get_by_role("link", name="Bestellübersicht Kantine")).to_be_visible()
    expect(page.get_by_role("link", name="Gerichte hinzufügen")).to_be_visible()
    expect(page.get_by_role("link", name="Essensplans Anlegen")).to_be_visible()


def test_register_hungernder(page: Page, load_users, delete_all_users):
    users = load_users
    admin_user = next(user for user in users if user.get("role") == "admin")
    new_user = next(user for user in users if user.get("role") == "new_user")
    perform_login(page, admin_user["email"], admin_user["password"])

    page.get_by_role("button", name="Menu").click()
    page.get_by_role("link", name="Benutzer Registrieren").click()
    page.wait_for_load_state('networkidle')
    page.get_by_label("Nachname*").click()
    page.get_by_label("Nachname*").fill(new_user["lastName"])
    page.get_by_label("Vorname*").click()
    page.get_by_label("Vorname*").fill(new_user["firstName"])
    page.get_by_label("E-Mail*").click()
    page.get_by_label("E-Mail*").fill(new_user["email"])
    page.get_by_label("E-Mail*").click()
    page.get_by_label("Rolle*").select_option("hungernde")
    page.get_by_label("Passwort*", exact=True).click()
    page.get_by_label("Passwort*", exact=True).fill(new_user["password"])
    page.get_by_label("Bestätige Passwort*").click()
    page.get_by_label("Bestätige Passwort*").fill(new_user["password"])
    page.get_by_role("button", name="Registrieren").click()
    perform_logout(page)
    perform_login(page, new_user["email"], new_user["password"])
    expect(page).to_have_url("/#/")
    page.get_by_role("button", name="Menu").click()
    expect(page.get_by_role("link", name="Bestellübersicht Benutzer")).to_be_visible()
    expect(page.get_by_role("link", name="Menüvorschlag")).to_be_visible()
