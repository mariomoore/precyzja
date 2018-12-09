#!/usr/bin/python

import pygame
from pygame.locals import *
import random
from pomiar_odleglosci import *

# stałe związane z ekranem
SZEROKOSC = 320
WYSOKOSC = 240
POZ = 20

# kolory
CZERWONY = (255, 0, 0)
ZIELONY = (0, 255, 0)

# stałe związane z pomiarem odległości
POMIARMIN = 5.0
POMIARMAX = 29.0

# elementy gry
przeszkody_gora = [0] * SZEROKOSC
przeszkody_dol = [0] * SZEROKOSC
pozycje_gracza = [0] * POZ

# hardware
czujnik = Czujnik_odleglosci(TRIG, ECHO)
d = Diody(REDLED, GREENLED, BLUELED)

def dodaj_przeszkody():
    skala = 10 # stała do przeskalowania kroku
    
    ostatnia_przeszkoda_gora = przeszkody_gora[-1]
    krok = random.randint(-1, 1)
    ostatnia_przeszkoda_gora += krok*skala
    if ostatnia_przeszkoda_gora < 0:
        ostatnia_przeszkoda_gora = 0
    
    ostatnia_przeszkoda_dol = przeszkody_dol[-1]
    krok = random.randint(-1, 1)
    ostatnia_przeszkoda_dol += krok*skala
    if ostatnia_przeszkoda_dol < 0:
        ostatnia_przeszkoda_dol = 0
    
    if WYSOKOSC - ostatnia_przeszkoda_gora - ostatnia_przeszkoda_dol < 8*skala:
        ostatnia_przeszkoda_gora -= skala
        ostatnia_przeszkoda_dol -= skala
    
    przeszkody_gora.append(ostatnia_przeszkoda_gora)
    przeszkody_gora.pop(0)

    przeszkody_dol.append(ostatnia_przeszkoda_dol)
    przeszkody_dol.pop(0)

def cm_na_pix(centymetry):
    return int((centymetry - POMIARMIN)*((WYSOKOSC - 1)/(POMIARMAX-POMIARMIN)))

def dodaj_pozycje_gracza():
    ostatna_pozycja = pozycje_gracza[-1]
    dystans = czujnik.pomiar()
    if dystans < POMIARMIN:
        d.ustaw_diody(REDLED)
        pozycje_gracza.append(ostatna_pozycja)
    elif dystans > POMIARMAX:
        d.ustaw_diody(BLUELED)
        pozycje_gracza.append(ostatna_pozycja)
    else:
        d.ustaw_diody(GREENLED)
        pozycje_gracza.append(WYSOKOSC-cm_na_pix(dystans))
    pozycje_gracza.pop(0)

def rysuj():
    screen = pygame.Surface((SZEROKOSC, WYSOKOSC))
    
    for i in range(SZEROKOSC):
        pygame.draw.line(screen, ZIELONY, [i, 0], [i, przeszkody_gora[i]], 1)
        pygame.draw.line(screen, ZIELONY, [i, WYSOKOSC], [i, WYSOKOSC-przeszkody_dol[i]], 1)

    for i in range(len(pozycje_gracza)):
        pygame.draw.circle(screen, CZERWONY, [i, pozycje_gracza[i]], 1)
    
    return screen
    
def kolizja():
    if ((pozycje_gracza[-1]) < przeszkody_gora[POZ-1]) or (WYSOKOSC - pozycje_gracza[-1] < przeszkody_dol[POZ-1]):
        return True
    return False

def main():
    pygame.init()
    screen = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
    pygame.display.set_caption('Precyzja')
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
    clock = pygame.time.Clock()
    
    while True:
        clock.tick(20)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                   pygame.quit()
                   return
        screen.blit(background, (0, 0))
        dodaj_przeszkody()
        dodaj_pozycje_gracza()
        if kolizja():
            pygame.quit()
            print("Kolizja")
            return
        screen.blit(rysuj(), (0, 0))
        pygame.display.flip()
    
if __name__ == '__main__':
    main()