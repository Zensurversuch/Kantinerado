import { Injectable } from '@angular/core';
import { MatSnackBar, MatSnackBarConfig } from '@angular/material/snack-bar';
import { Router, NavigationStart } from '@angular/router';
import { filter } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class FeedbackService {
  constructor(private snackBar: MatSnackBar, private router: Router) {
    this.router.events.pipe(
      filter(event => event instanceof NavigationStart)
    ).subscribe(() => {
      this.dismissSnackbar(); // Snackbar beim Neuladen der Seite schließen
    });
  }

  displayMessage(message: string) {
    if (!message) {
      return;
    }

    const messageType = this.extractMessageType(message);
    const config = new MatSnackBarConfig();

    config.horizontalPosition = 'center';
    config.verticalPosition = 'bottom';

    console.log("MessageType: " + messageType);
    switch (messageType) {
      case 'Erfolgreich:':
        config.panelClass = ['success-snackbar'];
        config.duration = 3000;
        break;
      case 'Fehler:':
        config.panelClass = ['error-snackbar'];
        config.duration = 10000;
        break;
      case 'Warnung:':
        config.panelClass = ['warning-snackbar'];
        config.duration = 5000;
        break;
      default:
        config.panelClass = [];
        break;
    }

    const messageWithoutType = message.replace(/(Erfolgreich|Fehler|Warnung):/, '').trim();

    this.snackBar.open(messageWithoutType, 'Schließen', config);
  }

  private extractMessageType(message: string): string {
    const matches = message.match(/(Erfolgreich|Fehler|Warnung):/);
    if (matches && matches.length > 0) {
      return matches[0].trim();
    }
    return '';
  }

  private dismissSnackbar() {
    this.snackBar.dismiss();
  }
}
