# Zusammenfassung
Diese Zusammenfassung umfasst:
- Alle Funktionen, um eine Kennzeichenerkennung mit Hilfe von openCV zu erreichen.
- Wofür die Funktionen verwendet wurden
- Welche Parameter übergeben werden
- Was die Ergebnisse (returns) der Funktionen sind

## Funktionalitäten:
- Umwandlung in ein Graustufenbild
- Erkennung von Kanten
- Erkennung von Konturen
- Erkennen von Rechtecken (= Kennzeichen)
- Ausschneiden der Rechtecke

## Graustufenbild
grayscale_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

- BGR = Blue, Green, Red
- OpenCV verwendet gewichtete Summe der Farbkanäle:
    - 0.114⋅B + 0.587⋅G + 0.299⋅R
    - Werte stammen aus TV-Norm ITU-R BT.601 und beschreiben, wie man aus einem Farbsignal eine Helligkeitskomponente (Luminanz) berechnet.
    - Gewichtung basiert auf der Wahrnehmung des menschlichen Auges – wir sind empfindlicher für Grün als für Blau (Wahrnehmung der Helligkeit)
- Pixelwerte liegen zwischen 0 (Schwarz) und 255 (Weiß)
- Grund:
    - Dimensionsreduktion: anstatt 10x10x3 bei RGB --> nur 300 Eingabewerte bei Graustufe
    - Ein statt drei dimensional
    - Algorithmen benötigen Graustufenbild als Eingabe

## Kantenerkennung
edges = cv.Canny(grayscale_img, 100, 200)
