import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="function")
def before_each(page: Page):
    page.goto('/#/')
    page.wait_for_load_state('networkidle')
    page.get_by_role('button', name='Menu').click()
    page.wait_for_load_state('networkidle')
    page.locator('li').filter(has_text='Login').click()
    page.get_by_role('button', name='Erstellen Sie einen Account').click()
    page.wait_for_load_state('networkidle')


def test_lastname_information(page: Page, before_each):
    information_locator = page.get_by_text('Nachname ist erforderlich.')
    expect(information_locator).to_be_hidden()
    page.get_by_label('Nachname*').click()
    page.get_by_text('Nachname*').click()
    expect(information_locator).to_be_visible()
    page.get_by_label('Nachname*').fill('Nachname')
    page.get_by_text('Nachname*').click()
    expect(information_locator).to_be_hidden()


def test_firstname_information(page: Page, before_each):
    information_locator = page.get_by_text('Vorname ist erforderlich.')
    expect(information_locator).to_be_hidden()
    page.get_by_label('Vorname*').click()
    page.get_by_text('Vorname*').click()
    expect(information_locator).to_be_visible()
    page.get_by_label('Vorname*').fill('Vorname')
    page.get_by_text('Vorname*').click()
    expect(information_locator).to_be_hidden()


def test_email_information(page: Page, before_each):
    information_locator = page.get_by_text('Bitte geben Sie eine gültige E-Mail-Adresse ein.')
    expect(information_locator).to_be_hidden()
    page.get_by_label('E-Mail*').click()
    page.get_by_text('E-Mail*').click()
    expect(information_locator).to_be_visible()
    page.get_by_label('E-Mail*').fill('email')
    page.get_by_text('E-Mail*').click()
    expect(information_locator).to_be_visible()
    page.get_by_label('E-Mail*').fill('email@test.com')
    page.get_by_text('E-Mail*').click()
    expect(information_locator).to_be_hidden()


def test_password_information(page: Page, before_each):
    information_locator = page.get_by_text(
        'Mindestens 8 Zeichen, eine Zahl, Sonderzeichen und Großbuchstabe erforderlich.')
    text_field_locator = page.get_by_label('Passwort*', exact=True)
    expect(information_locator).to_be_hidden()
    text_field_locator.click()
    page.get_by_text('Passwort*', exact=True).click()
    expect(information_locator).to_be_visible()
    text_field_locator.fill('test')
    expect(information_locator).to_be_visible()
    text_field_locator.fill('Test')
    expect(information_locator).to_be_visible()
    text_field_locator.fill('test_')
    expect(information_locator).to_be_visible()
    text_field_locator.fill('Test_')
    expect(information_locator).to_be_visible()
    text_field_locator.fill('1234')
    expect(information_locator).to_be_visible()
    text_field_locator.fill('Test1')
    expect(information_locator).to_be_visible()
    text_field_locator.fill('Test_1')
    expect(information_locator).to_be_visible()
    text_field_locator.fill('passwort')
    expect(information_locator).to_be_visible()
    text_field_locator.fill('Passwort')
    expect(information_locator).to_be_visible()
    text_field_locator.fill('Passwort_')
    expect(information_locator).to_be_visible()
    text_field_locator.fill('Tests_0!')
    text_field_locator.click()
    expect(information_locator).to_be_hidden()


def test_confirm_password_information(page: Page, before_each):
    confirmation_locator = page.get_by_text('Passwortbestätigung ist erforderlich.')
    equal_locator = page.get_by_text('Die Passwörter stimmen nicht überein.')
    expect(confirmation_locator).to_be_hidden()
    expect(equal_locator).to_be_hidden()
    page.get_by_label('Bestätige Passwort*').click()
    page.get_by_text('Bestätige Passwort*').click()
    expect(confirmation_locator).to_be_visible()
    expect(equal_locator).to_be_hidden()
    page.get_by_label('Bestätige Passwort*').fill('Tests_0!')
    page.get_by_text('Bestätige Passwort*').click()
    expect(confirmation_locator).to_be_hidden()
    expect(equal_locator).to_be_visible()
    page.get_by_label('Passwort*', exact=True).fill('Tests_0!')
    page.get_by_text('Bestätige Passwort*').click()
    expect(confirmation_locator).to_be_hidden()
    expect(equal_locator).to_be_hidden()
