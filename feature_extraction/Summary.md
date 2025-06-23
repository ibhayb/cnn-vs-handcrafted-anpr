# Zusammenfassung
Diese Zusammenfassung umfasst:
- Alle Funktionen, um eine Kennzeichenerkennung mit Hilfe von openCV zu erreichen.
- Wofür die Funktionen verwendet wurden
- Welche Parameter übergeben werden
- Was die Ergebnisse (returns) der Funktionen sind

## Funktionalitäten:
- Umwandlung in ein Graustufenbild
- Reduzierung von Rauschen
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
    [1, 2, 1],
    [2, 4, 2],
    [1, 2, 1]
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
- Diese markieren die Objektgrenzen (mit starken Intensitätsunterschieden (Helligkeit))
- Sehr sensibel gegenüber Rauschen, daher vorher das Bild mit GaussianBlur glätten, um falsche Kanten zu vermeiden
- Durchführung:
    1. Berechnung des Gradienten: Vektor, der zeigt, wo und wie schnell sich die Intensität ändert. Dies erfolgt mit dem Sobel-Operator in X- und Y-Richtung.
    Gx = [-1, 0, 1],        Gy = [-1, -2, -1],
         [-2, 0, 2],             [0, 0, 0],
         [-1, 0, 1]              [1, 2, 1]
    Mit diesem werden die Ableitungen in X- und Y-Richtung berechnet:
    Img_x = Img * Gx; Img_y = Img * Gy
    2. Gradient-Stärke und Richtung:
    Gradient-Stärke: M(x, y) = sqrt(Img_x^2 + Img_y^2)
    Gradient-Richtung: Theta(x, y) = arctan(Img_x^2 / Img_y^2)
    --> Die Richtung zeigt Senkrecht zur Kante!
    --> Die Stärke gibt an, wie stark sich die Helligkeit an dieser Stelle im Bild ändert.
    --> Gradient zeigt in die Richtung wo es Heller wird!
    3. Non-Maximum Suppression (NMS): Die Kanten sollen 1 Pixel breit sein, ohne NMS hätten wir breite Pixel. Filtert alles außer dem lokalen Maximum. Dazu wird bei jedem Pixel geprüft, ob es sich in seiner Umgebung in Gradientenrichtung um ein lokales Maximum handelt. Das Maximum wird behalten und die anderen Werte werden auf Null gesetzt. Dadurch erhalten wir dünne Kanten. Ohne NMS würde wir dicke und mehrzeilige Kanten erhalten.
    ![Alt text](https://docs.opencv.org/4.x/nms.jpg)
    --> Bildbeschreibung: Point A is on the edge ( in vertical direction). Gradient direction is normal to the edge. Point B and C are in gradient directions. So point A is checked with point B and C to see if it forms a local maximum. If so, it is considered for next stage, otherwise, it is suppressed ( put to zero).
    4. Hysteresis Thresholding: Setze eine untere und obere Grenze für die Gradientenstärke, um nach bestimmten Kanten zu filtern. Beispiel:
    Obere Grenze = 100, untere Grenze = 50 --> Alles was unterhalb der unteren Grenze ist verwerfen. Alles was oberhalb der oberen Grenze ist, ist sicher eine Kante. Alles was dazwischen ist, sind mögliche Kanten, diese nur behalten, wenn sie mit starken Kanten verbunden sind, ansonsten werden diese rausgeschmissen. In dieser Phase werden auch kleine Pixelstörungen entfernt, da davon ausgegangen wird, dass es sich bei den Kanten um lange Linien handelt.
    ![Alt text](https://docs.opencv.org/4.x/hysteresis.jpg)
    --> Bildbeschreibung: The edge A is above the maxVal, so considered as "sure-edge". Although edge C is below maxVal, it is connected to edge A, so that also considered as valid edge and we get that full curve. But edge B, although it is above minVal and is in same region as that of edge C, it is not connected to any "sure-edge", so that is discarded. So it is very important that we have to select minVal and maxVal accordingly to get the correct result.
