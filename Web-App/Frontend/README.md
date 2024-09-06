# Frontend

Dieses Projekt wurde mit der [Angular CLI](https://github.com/angular/angular-cli) Version 17.2.0 erstellt.

## Voraussetzungen

Stellen Sie sicher, dass die folgenden Tools installiert sind, bevor Sie fortfahren:

1. [Node.js](https://nodejs.org/) (mindestens Version 22.5.1 oder höher)
2. [Angular CLI](https://angular.io/cli) (mindestens Version 17.2 oder höher)
<ul>
<li> <a href="https://playwright.dev/">Playwright</a> (wird über <code>npx</code> ausgeführt)</li>
<li> <a href="https://angular.io/cli">Angular</a> (wird über <code>ng</code> ausgeführt)</li>
</ul>

Falls diese Tools nicht installiert sind, können Sie sie wie folgt installieren:
```bash
npm install
```

## Angular Entwicklungsserver starten

Angular bietet die Möglichkeit, einen Entwicklungsserver zu starten. Dies ist besonders nützlich, um Änderungen in der Anwendung sofort zu sehen. Es wird empfohlen, das Backend bzw. die Datenbank parallel zu starten, da einige Funktionen sonst möglicherweise nicht verfügbar sind.
Um den Entwicklungsserver zu starten, verwenden Sie den folgenden Befehl:


```bash
ng serve
```

Der Server wird bei jeder Änderung des Codes automatisch neu geladen.
# Anleitung: Tests in einem Angular-Projekt ausführen

In diesem Abschnitt erfahren Sie, wie Sie End-to-End-Tests (e2e) mit Playwright und den Angular-Testserver ausführen.

### End-to-End (e2e) Tests mit Playwright starten:

Um die e2e-Tests auszuführen, verwenden Sie den folgenden Befehl:
```bash
npx playwright test
```

Playwright ermöglicht das Testen von Benutzerinteraktionen in verschiedenen Browsern. Dieser Befehl führt alle im Projekt definierten Playwright-Tests aus.
### Code erstellen:
```bash
npx playwright codegen
```
Dieser Befehl öffnet einen Browser (in der Regel Chromium), in dem Sie Ihre Anwendung manuell testen können. Während Sie dies tun, wird automatisch Code generiert, der als Playwright-Test dient. 
Hinweis: Beim Schließen des Browsers wird auch das Playwright-Codefenster geschlossen.
### Code debuggen:
```bash
npx playwright test --debug
```
Dieser Befehl ermöglicht das Debuggen von Tests. Es bietet eine visuelle Darstellung, um den Ablauf der Tests Schritt für Schritt nachzuvollziehen.

### Die Playwright UI öffnen:
```bash
npx playwright test --ui
```
Die Playwright-Benutzeroberfläche zeigt Testläufe an und ermöglicht es Ihnen, vergangene Testläufe zu inspizieren und Details zu Fehlern zu sehen. Dies ist besonders hilfreich, um nach einem fehlgeschlagenen Test den Grund zu ermitteln.
