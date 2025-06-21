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

## GaussianBlur
blurred = cv.GaussianBlur(grayscale_img, (3, 3), 0)

- Low pass filter (LFP)
- Bildglättung bzw. Rauschreduzierung
- Aktion ist eine Kernel Convolution
- Kernel von Größe z.B. 3x3, 5x5, 7x7 (muss ungerade sein, damit es eine Mitte gibt)
- Je größer, desto stärker wird geglättet (aber auch details verschwinden)
- Kernel z.B. 3x3:
    [[1, 2, 1],
    [2, 4, 2],
    [1, 2, 1]]
    wird über ein Pixel im Bild gelegt. Anschließend werden übereinanderliegende Pixel miteinander multipliziert, die Summe aus allen Pixeln berechnet und durch 16 geteilt (Summe des Kernels) --> Neuer Wert des Pixels im Bild.
- Parameter:
    - src: meist Graustufenbild
    - ksize: Kernelgröße (wie viele Nachbarpixel einbezogen werden)
    - sigmaX: Steuert, wie breit die Gauß-Kurve ist → wie stark benachbarte Pixel noch "zählen". Wenn sigmaX klein ist: nur nahe Pixel zählen viel. Wenn sigmaX groß ist: auch weiter entfernte Pixel zählen viel.
    - sigmaY (Optional): Wenn du nichts angibst (oder 0 setzt), wird einfach sigmaY = sigmaX verwendet. Du kannst also auch horizontal und vertikal unterschiedlich stark glätten, falls du willst.
- Wenn 0 für sigmaX --> OpenCV berechnet automatisch einen passenden sigma basierend auf der Kernelgröße
- Sigma und Kernelgröße (ksize) müssen aufeinander abgestimmt sein, da ein zu kleiner Kernel bei großem Sigma die Gauß-Verteilung nicht vollständig abdecken kann und so zu ungenauen Glättungsergebnissen führt.
- Kleines sigma: ist die Glocke steil wie ein Berg --> nur die Mitte zählt (stärkeres Gewicht im mittlerem Pixel)
- Großes sigma: ist die Glocke flach wie ein Hügel --> auch die Ränder des Kernels bekommen Gewicht (kein großer Unterschied im Gewicht zum mittleren Pixel)
- Je größer das sigma, desto stärker wird das Bild verwischt.
- Je kleiner das sigma, nur nahe Pixel haben Einfluss --> Glättung ist lokal und schwach. Details bleiben eher erhalten.

## Kantenerkennung
edges = cv.Canny(grayscale_img, 100, 200)

- High pass filter (HPF)
- Methode zur Kantenerkennung in Bildern
- Diese markieren die Objektgrenzen
- Sehr sensibel gegenüber Rauschen, daher vorher das Bild mit GaussianBlur glätten, um falsche Kanten zu vermeiden
-
