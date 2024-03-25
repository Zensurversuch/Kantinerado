import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar'; // Importiere MatSnackBar

@Injectable({
  providedIn: 'root'
})
export class ErrorService {
  constructor(private snackBar: MatSnackBar) {}

  displayErrorMessage(message: string) {
    this.snackBar.open(message, 'Schließen', {
      duration: 5000, // Anzeigedauer in Millisekunden (hier: 5 Sekunden)
      horizontalPosition: 'center',
      verticalPosition: 'bottom'
    });
  }
}



// Erfolgreich
// 