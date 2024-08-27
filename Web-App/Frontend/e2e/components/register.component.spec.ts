import {test, expect} from '@playwright/test';

test.beforeEach(async ({page}) => {
  await page.goto('http://localhost:4200/#/register');
})
/*
test('test', async ({page}) => {
  await page.goto('http://localhost:4200/');
  await page.goto('http://localhost:4200/#/');
  await page.getByRole('button', {name: 'Menu'}).click();
  await page.locator('li').filter({hasText: 'Login'}).click();
  await page.getByRole('button', {name: 'Erstellen Sie einen Account'}).click();
  await page.getByLabel('Nachname*').click();
  await page.getByLabel('Vorname*').click();
  await page.getByText('Nachname ist erforderlich.').click();
  await page.getByText('Vorname ist erforderlich.').click();
  await page.getByLabel('E-Mail*').click();
  await page.getByText('Bitte geben Sie eine gültige').click();
  await page.getByLabel('Passwort*', {exact: true}).click();
  await page.getByText('Passwort*', {exact: true}).click();
  await page.getByText('Mindestens 8 Zeichen, eine').click();
  await page.getByLabel('Passwort*', {exact: true}).click();
  await page.getByLabel('Passwort*', {exact: true}).fill('Schmidt1234');
  await page.getByLabel('Passwort*', {exact: true}).click();
  await page.getByLabel('Passwort*', {exact: true}).fill('gutes_Passwort_1');
  await page.getByLabel('Bestätige Passwort*').click();
  await page.getByLabel('Bestätige Passwort*').fill('h');
  await page.getByText('Passwortbestätigung ist').click();
  await page.getByText('Die Passwörter stimmen nicht').click();
  await page.getByLabel('Bestätige Passwort*').click();
  await page.getByLabel('Bestätige Passwort*').fill('gutes_Passwort_1');
  await page.getByLabel('E-Mail*').click();
  await page.getByLabel('E-Mail*').fill('TestUser@tes');
  await page.getByLabel('E-Mail*').click();
  await page.getByLabel('E-Mail*').fill('TestUser@testEmail.com');
  await page.locator('body').click();
  await page.getByLabel('Nachname*').click();
  await page.getByLabel('Nachname*').fill('User');
  await page.getByLabel('Vorname*').click();
  await page.getByLabel('Vorname*').fill('Test');
  await page.locator('body').click();
});
*/

test.describe('Testing failure in the registration Form', () => {
  test('should be true if the failure for "Nachname" ist shown.', async ({page}) => {
    const informationLocator = page.getByText('Nachname ist erforderlich.')
    expect(informationLocator.isHidden())
    await page.getByText('Nachname*').click();
    expect(informationLocator.isVisible())
    await page.getByLabel('Nachname*').fill('Nachname');
    await page.getByText('Nachname*').click();
    expect(informationLocator.isHidden())
  })
  test('should be true if the failure for "Vorname" ist shown.', async ({page}) => {
    const informationLocator = page.getByText('Vorname ist erforderlich.')
    expect(informationLocator.isHidden())
    await page.getByText('Vorname*').click();
    expect(informationLocator.isVisible())
    await page.getByLabel('Vorname*').fill('Vorname');
    await page.getByText('Vorname*').click();
    expect(informationLocator.isHidden())
  })
  test('should be true if the failure for "E-Mail" ist shown.', async ({page}) => {
    const informationLocator = page.getByText('Bitte geben Sie eine gültige E-Mail-Adresse ein.')
    expect(informationLocator.isHidden())
    await page.getByText('E-Mail*').click();
    expect(informationLocator.isVisible())
    await page.getByLabel('E-Mail*').fill('email');
    expect(informationLocator.isVisible())
    await page.getByLabel('E-Mail*').fill('email@test.com');
    await page.getByText('E-Mail*').click();
    expect(informationLocator.isHidden())
  })
  test('should be true if the failure for "Passwort" ist shown.', async ({page}) => {
    const informationLocator = page.getByText('Mindestens 8 Zeichen, eine Zahl, Sonderzeichen und Großbuchstabe erforderlich.')
    const labelLocator = page.getByText('Passwort*', {exact: true})
    expect(informationLocator.isHidden())
    await labelLocator.click();
    expect(informationLocator.isVisible())
    await labelLocator.fill('test');
    expect(informationLocator.isVisible())
    await labelLocator.fill('Test');
    expect(informationLocator.isVisible())
    await labelLocator.fill('test_');
    expect(informationLocator.isVisible())
    await labelLocator.fill('Test_');
    expect(informationLocator.isVisible())
    await labelLocator.fill('1234');
    expect(informationLocator.isVisible())
    await labelLocator.fill('Test1');
    expect(informationLocator.isVisible())
    await labelLocator.fill('Test_1');
    expect(informationLocator.isVisible())
    await labelLocator.fill('passwort');
    expect(informationLocator.isVisible())
    await labelLocator.fill('Passwort');
    expect(informationLocator.isVisible())
    await labelLocator.fill('Passwort_');
    expect(informationLocator.isVisible())
    await labelLocator.fill('Tests_0!');
    await labelLocator.click();
    expect(informationLocator.isHidden())
  })

})
