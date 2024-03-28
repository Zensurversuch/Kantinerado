import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ImageService {

  constructor() { }

  // Funktion zur Kodierung eines Bildes in Base64
  encodeImage(image: File): Promise<string> {
    return new Promise<string>((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => {
        resolve(reader.result as string);
      };
      reader.onerror = reject;
      reader.readAsDataURL(image);
    });
  }

  // Funktion zur Dekodierung einer Base64-kodierten Zeichenfolge in ein Bild
  decodeImage(base64String: string): Promise<Blob> {
    return fetch(base64String)
      .then(response => response.blob());
  }
}