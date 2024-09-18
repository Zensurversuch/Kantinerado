import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="function")
def before_each(page: Page):
    page.goto('/')
    page.wait_for_load_state('networkidle')
    page.get_by_role('button', name='Menu').click()
    page.wait_for_load_state('networkidle')
    page.locator('li').filter(has_text='Login').click()
    page.get_by_role('button', name='Erstellen Sie einen Account').click()
    page.wait_for_load_state('networkidle')

"""should be true if the failure for "Nachname" ist shown."""
def test_lastname_information(page:Page, before_each):
    information_locator = page.get_by_text('Nachname ist erforderlich.')
    expect(information_locator).to_be_hidden()
    page.get_by_label('Nachname*').click()
    page.get_by_text('Nachname*').click()
    expect(information_locator).to_be_visible()
    page.get_by_label('Nachname*').fill('Nachname')
    page.get_by_text('Nachname*').click()
    expect(information_locator).to_be_hidden()
'''
  test('should be true if the failure for "Vorname" ist shown.', async ({page}) => {
    const informationLocator = page.getByText('Vorname ist erforderlich.');
    await expect(informationLocator).toBeHidden();
    await page.getByLabel('Vorname*').click();
    await page.getByText('Vorname*').click();
    await expect(informationLocator).toBeVisible();
    await page.getByLabel('Vorname*').fill('Vorname');
    await page.getByText('Vorname*').click();
    await expect(informationLocator).toBeHidden();
  })
  test('should be true if the failure for "E-Mail" ist shown.', async ({page}) => {
    const informationLocator = page.getByText('Bitte geben Sie eine gültige E-Mail-Adresse ein.');
    await expect(informationLocator).toBeHidden();
    await page.getByLabel('E-Mail*').click();
    await page.getByText('E-Mail*').click();
    await expect(informationLocator).toBeVisible();
    await page.getByLabel('E-Mail*').fill('email');
    await page.getByText('E-Mail*').click();
    await expect(informationLocator).toBeVisible();
    await page.getByLabel('E-Mail*').fill('email@test.com');
    await page.getByText('E-Mail*').click();
    await expect(informationLocator).toBeHidden();
  })
  test('should be true if the failure for "Passwort" ist shown.', async ({page}) => {
    const informationLocator = page.getByText('Mindestens 8 Zeichen, eine Zahl, Sonderzeichen und Großbuchstabe erforderlich.')
    const textFieldLocator = page.getByLabel('Passwort*', {exact: true})
    await expect(informationLocator).toBeHidden();
    await textFieldLocator.click();
    await page.getByText('Passwort*', {exact: true}).click();
    await expect(informationLocator).toBeVisible();
    await textFieldLocator.fill('test');
    await expect(informationLocator).toBeVisible();
    await textFieldLocator.fill('Test');
    await expect(informationLocator).toBeVisible();
    await textFieldLocator.fill('test_');
    await expect(informationLocator).toBeVisible();
    await textFieldLocator.fill('Test_');
    await expect(informationLocator).toBeVisible();
    await textFieldLocator.fill('1234');
    await expect(informationLocator).toBeVisible();
    await textFieldLocator.fill('Test1');
    await expect(informationLocator).toBeVisible();
    await textFieldLocator.fill('Test_1');
    await expect(informationLocator).toBeVisible();
    await textFieldLocator.fill('passwort');
    await expect(informationLocator).toBeVisible();
    await textFieldLocator.fill('Passwort');
    await expect(informationLocator).toBeVisible();
    await textFieldLocator.fill('Passwort_');
    await expect(informationLocator).toBeVisible();
    await textFieldLocator.fill('Tests_0!');
    await textFieldLocator.click();
    await expect(informationLocator).toBeHidden();
  })
  test('should be true if the failure for "Bestätige Passwort" ist shown.', async ({page}) => {
    const confirmationLocator = page.getByText('Passwortbestätigung ist erforderlich.');
    const equalLocator = page.getByText('Die Passwörter stimmen nicht überein.');
    await expect(confirmationLocator).toBeHidden();
    await expect(equalLocator).toBeHidden();
    await page.getByLabel('Bestätige Passwort*').click();
    await page.getByText('Bestätige Passwort*').click();
    await expect(confirmationLocator).toBeVisible();
    await expect(equalLocator).toBeHidden();
    await page.getByLabel('Bestätige Passwort*').fill('Tests_0!');
    await page.getByText('Bestätige Passwort*').click();
    await expect(confirmationLocator).toBeHidden();
    await expect(equalLocator).toBeVisible();
    await page.getByLabel('Passwort*', {exact: true}).fill('Tests_0!');
    await page.getByText('Bestätige Passwort*').click();
    await expect(confirmationLocator).toBeHidden();
    await expect(equalLocator).toBeHidden();
  })
})

'''
