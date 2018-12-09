Raspberry Pi 3 Model B+
=======================

Gra Precyzja
------------

W tym repozytorium znajduje się kod źródłowy gry wykorzystującej czujnik
odległości HC-SR04. Zmierzona odległość steruje położeniem czerwonej kropki na
ekranie (do sterowania odległością warto użyć np. kartki papieru, a nie ręki).
Zderzenie się kropki z zieloną przeszkodą powoduje koniec gry. Pomiar odbywa
się w odległości 5cm - 29cm od czujnika i w tym zakresie świeci się zielona
dioda. Poniżej 5cm świeci się czerwona, a powyżej 29cm - niebieska.

Skrypt uruchamia się:

    python3 precyzja.py

![schemat podłączenia układu do Raspberry Pi](/schemat.png "Schemat")
