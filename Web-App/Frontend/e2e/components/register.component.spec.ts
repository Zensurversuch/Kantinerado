import {test, expect} from '@playwright/test';

test.beforeEach(async ({page}) => {
  await page.goto('http://localhost:4200/#/register');
})

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
