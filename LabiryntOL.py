"""
LabiryntOL - prosta gra labiryntowa (wersja testowa)
Żółwik ucieka z labiryntu, krab próbuje go złapać.

Sterowanie: strzałki lub WASD
Spacja - zostaw pieska (co 20 s), Enter - start / następny poziom
P - nowa gra od poziomu 1, K - klawiszologia
F11 - pełny ekran / okno
Esc - wyjście z pełnego ekranu (w oknie: wyjście z gry)

Wymaga: pip install pygame-ce   (lub: pip install pygame)
"""

import io
import math
import os
import random
import struct
import sys
from collections import deque

import pygame

# ---------------------------------------------------------------------------
# Ustawienia
# ---------------------------------------------------------------------------
NAZWA = "LabiryntOL"
WERSJA = "1.2.0.1"

KOLUMNY = 31          # liczba kafli w poziomie (nieparzysta)
WIERSZE = 21          # liczba kafli w pionie (nieparzysta)
KAFEL = 32            # rozmiar kafla w pikselach
PASEK = 60            # wysokość paska informacyjnego u góry
FPS = 60

KROK_ZOLWIA = 0.13    # sekundy na jeden krok żółwia (przy wciśniętym klawiszu)
# Poziomy trudności: wartość na poziomie 1, zmiana na każdy kolejny poziom, granica.
KROK_KRABA = (0.32, -0.015, 0.20)     # sekundy na krok kraba (mniej = szybszy)
START_KRABA = (3.0, -0.25, 1.0)       # po tylu sekundach rusza pierwszy krab
NOWY_KRAB_CO = (20.0, -1.5, 10.0)     # co tyle sekund pojawia się nowy krab
PRZEJSCIA = (0.14, -0.01, 0.05)       # część ścian usuwanych, by powstały pętle
KRAB_WIECEJ_CO = 4    # co tyle poziomów o jednego kraba więcej na starcie (poz. 5, 9)
MAX_KRABOW_START = 3  # najwięcej krabów na starcie poziomu
ODNOGI_STARTU = 1 / 3 # ze startu wychodzą 2 osobne drogi o długości >= tej części szerokości planszy
POJAWIANIE = 1.0      # tyle sekund nowy krab miga, zanim ruszy (jest wtedy niegroźny)
MIN_ODLEGLOSC = 8     # minimalna odległość (w krokach) nowego kraba od żółwia
PIESEK_CO = 20.0      # co tyle sekund można zostawić pieska (spacja)
ZATRZYMANIE = 3.0     # na tyle sekund piesek zatrzymuje kraba

PLIK_IKONY = "ikona.ico"

SZER = KOLUMNY * KAFEL
WYS = WIERSZE * KAFEL + PASEK

# Kolory
TLO = (24, 28, 40)
SCIANA = (70, 90, 130)
SCIANA_JASNA = (100, 125, 170)
PODLOGA = (225, 215, 185)
WYJSCIE = (90, 200, 110)
TEKST = (240, 240, 240)
ZOLW_SKORUPA = (40, 140, 60)
ZOLW_WZOR = (25, 95, 40)
ZOLW_SKORA = (140, 200, 90)
KRAB = (220, 60, 50)
KRAB_CIEMNY = (150, 30, 30)
YORK_SIERSC = (95, 110, 135)     # stalowoniebieski grzbiet
YORK_PODPALANE = (205, 155, 85)  # podpalana głowa i łapki
YORK_KOKARDA = (230, 50, 90)

SCIANA_T, PUSTE_T = 1, 0

KLAWISZOLOGIA = [
    ("Strzałki / W A S D", "ruch żółwika"),
    ("Spacja", "zostaw pieska (co 20 s)"),
    ("Enter", "start / następny poziom / powtórz poziom"),
    ("P", "nowa gra od poziomu 1"),
    ("K", "pokaż / ukryj klawiszologię"),
    ("F11", "pełny ekran / okno"),
    ("Esc", "z pełnego ekranu do okna; w oknie – wyjście z gry"),
]

KIERUNKI = {
    pygame.K_UP: (0, -1), pygame.K_w: (0, -1),
    pygame.K_DOWN: (0, 1), pygame.K_s: (0, 1),
    pygame.K_LEFT: (-1, 0), pygame.K_a: (-1, 0),
    pygame.K_RIGHT: (1, 0), pygame.K_d: (1, 0),
}


def wartosc_poziomu(parametr, poziom):
    """Wartość parametru (start, zmiana, granica) na danym poziomie."""
    poczatek, zmiana, granica = parametr
    w = poczatek + zmiana * (poziom - 1)
    return max(w, granica) if zmiana < 0 else min(w, granica)


def liczba(x):
    """Liczba po polsku: 20 -> „20”, 18.5 -> „18,5”."""
    return f"{round(x, 1):g}".replace(".", ",")


def sciezka_zasobu(nazwa):
    """Ścieżka do pliku zasobu – działa ze skryptu i z wersji PyInstaller."""
    katalog = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(katalog, nazwa)


def wczytaj_ico(sciezka):
    """Wczytuje plik .ico. Pygame nie obsługuje ikon z obrazkami PNG w środku,
    więc w takim przypadku wyciągamy największy obrazek PNG ręcznie."""
    try:
        return pygame.image.load(sciezka)
    except pygame.error:
        pass
    with open(sciezka, "rb") as f:
        dane = f.read()
    liczba = struct.unpack_from("<H", dane, 4)[0]
    najlepszy, rozmiar_max = None, -1
    for i in range(liczba):
        w, h, _, _, _, _, dlugosc, offset = struct.unpack_from("<BBBBHHII", dane, 6 + i * 16)
        obraz = dane[offset:offset + dlugosc]
        rozmiar = (w or 256) * (h or 256)
        if obraz.startswith(b"\x89PNG") and rozmiar > rozmiar_max:
            najlepszy, rozmiar_max = obraz, rozmiar
    if najlepszy is None:
        raise pygame.error("Nieobsługiwany format ikony")
    return pygame.image.load(io.BytesIO(najlepszy), "ikona.png")


def ustaw_ikone():
    try:
        pygame.display.set_icon(wczytaj_ico(sciezka_zasobu(PLIK_IKONY)))
    except (pygame.error, OSError, struct.error):
        pass  # brak lub błąd ikony nie blokuje gry


# ---------------------------------------------------------------------------
# Labirynt
# ---------------------------------------------------------------------------
def generuj_labirynt(kol, wier, przejscia):
    """Losuje labirynt, w którym ze startu wychodzą dwie osobne drogi o długości
    co najmniej 1/3 szerokości planszy, łączące się dopiero dalej (start leży na
    długiej pętli). Krab spotkany tuż po starcie zawsze da się obejść drugą drogą.
    Około 3/4 labiryntów spełnia ten warunek od razu – pozostałe losujemy ponownie,
    dzięki czemu trudność poziomu się nie zmienia."""
    start = (1, 1)
    dlugosc = max(2, round(kol * ODNOGI_STARTU))
    for _ in range(50):
        siatka, wyjscie, zapas = generuj_labirynt_raz(kol, wier, przejscia)
        if dobry_start(siatka, start, dlugosc):
            return siatka, wyjscie
    # awaryjnie (praktycznie się nie zdarza): otwieraj kolejne ściany
    while zapas and not dobry_start(siatka, start, dlugosc):
        x, y = zapas.pop()
        siatka[y][x] = PUSTE_T
    return siatka, wyjscie


def generuj_labirynt_raz(kol, wier, przejscia):
    """Generuje labirynt metodą DFS (recursive backtracker) na siatce kafli.
    Komórki mają nieparzyste współrzędne, ściany są pomiędzy nimi."""
    siatka = [[SCIANA_T] * kol for _ in range(wier)]
    start = (1, 1)
    siatka[1][1] = PUSTE_T
    stos = [start]
    while stos:
        x, y = stos[-1]
        sasiedzi = []
        for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)):
            nx, ny = x + dx, y + dy
            if 0 < nx < kol - 1 and 0 < ny < wier - 1 and siatka[ny][nx] == SCIANA_T:
                sasiedzi.append((nx, ny, dx, dy))
        if sasiedzi:
            nx, ny, dx, dy = random.choice(sasiedzi)
            siatka[y + dy // 2][x + dx // 2] = PUSTE_T
            siatka[ny][nx] = PUSTE_T
            stos.append((nx, ny))
        else:
            stos.pop()

    # Usuń część ścian wewnętrznych, by powstały pętle (łatwiej uciekać krabowi)
    kandydaci = []
    for y in range(1, wier - 1):
        for x in range(1, kol - 1):
            if siatka[y][x] != SCIANA_T:
                continue
            poziomo = siatka[y][x - 1] == PUSTE_T and siatka[y][x + 1] == PUSTE_T
            pionowo = siatka[y - 1][x] == PUSTE_T and siatka[y + 1][x] == PUSTE_T
            if poziomo != pionowo:
                kandydaci.append((x, y))
    random.shuffle(kandydaci)
    ile = int(len(kandydaci) * przejscia)
    for x, y in kandydaci[:ile]:
        siatka[y][x] = PUSTE_T
    zapas = kandydaci[ile:]          # ściany, które można jeszcze otworzyć

    # Wyjście na prawej krawędzi, w dolnej połowie
    wy = random.choice(range(wier // 2 | 1, wier - 1, 2))
    siatka[wy][kol - 1] = PUSTE_T
    wyjscie = (kol - 1, wy)

    # Start: żółw ma od razu dwie drogi – w prawo i w dół
    siatka[1][2] = PUSTE_T
    siatka[2][1] = PUSTE_T
    return siatka, wyjscie, zapas


def sasiedzi_pola(siatka, p):
    x, y = p
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if wolne(siatka, x + dx, y + dy):
            yield (x + dx, y + dy)


def blok_startu(siatka, start):
    """Pola leżące na wspólnej pętli ze startem (blok dwuspójny zawierający oba
    wyjścia ze startu). Do każdego z tych pól prowadzą ze startu dwie drogi
    bez wspólnych pól. Algorytm Tarjana, wersja bez rekurencji."""
    numer, niski = {start: 0}, {start: 0}
    licznik = 1
    stos_krawedzi = []
    stos = [(start, None, iter(list(sasiedzi_pola(siatka, start))))]
    while stos:
        u, rodzic, it = stos[-1]
        for v in it:
            if v == rodzic:
                continue
            if v not in numer:
                numer[v] = niski[v] = licznik
                licznik += 1
                stos_krawedzi.append((u, v))
                stos.append((v, u, iter(list(sasiedzi_pola(siatka, v)))))
                break
            if numer[v] < numer[u]:
                stos_krawedzi.append((u, v))
                niski[u] = min(niski[u], numer[v])
        else:
            stos.pop()
            if rodzic is None:
                continue
            niski[rodzic] = min(niski[rodzic], niski[u])
            if niski[u] >= numer[rodzic]:          # zamknięty blok
                blok = set()
                while True:
                    a, b = stos_krawedzi.pop()
                    blok.update((a, b))
                    if (a, b) == (rodzic, u):
                        break
                if rodzic == start and len(blok) > 2:
                    return blok
    return set()


def dobry_start(siatka, start, dlugosc):
    """True, gdy start leży na pętli, na której jest pole odległe od startu
    o co najmniej 'dlugosc' kroków – czyli ze startu wychodzą dwie osobne drogi
    o długości >= dlugosc, które dopiero potem się spotykają."""
    blok = blok_startu(siatka, start)
    if not blok:
        return False
    _, odl = najdalsze_pole(siatka, start)
    return max(odl[p] for p in blok) >= dlugosc


def wolne(siatka, x, y):
    return 0 <= y < len(siatka) and 0 <= x < len(siatka[0]) and siatka[y][x] == PUSTE_T


def nastepny_krok(siatka, skad, dokad):
    """BFS: zwraca pierwsze pole na najkrótszej drodze ze 'skad' do 'dokad'."""
    if skad == dokad:
        return skad
    poprzednik = {skad: None}
    kolejka = deque([skad])
    while kolejka:
        p = kolejka.popleft()
        if p == dokad:
            break
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (p[0] + dx, p[1] + dy)
            if n not in poprzednik and wolne(siatka, *n):
                poprzednik[n] = p
                kolejka.append(n)
    if dokad not in poprzednik:
        return skad
    p = dokad
    while poprzednik[p] != skad:
        p = poprzednik[p]
    return p


def najdalsze_pole(siatka, start):
    """Zwraca pole najdalsze (w krokach) od pola start."""
    odl = {start: 0}
    kolejka = deque([start])
    ostatnie = start
    while kolejka:
        p = kolejka.popleft()
        ostatnie = p
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (p[0] + dx, p[1] + dy)
            if n not in odl and wolne(siatka, *n):
                odl[n] = odl[p] + 1
                kolejka.append(n)
    return ostatnie, odl


# ---------------------------------------------------------------------------
# Postacie
# ---------------------------------------------------------------------------
class Postac:
    def __init__(self, x, y, czas_kroku):
        self.x, self.y = x, y            # pozycja logiczna (kafel)
        self.px, self.py = x, y          # pozycja poprzednia (do animacji)
        self.czas_kroku = czas_kroku
        self.postep = 1.0                # 0..1 – postęp animacji ruchu
        self.kierunek = (1, 0)
        self.czekaj = 0.0                # sekundy do rozpoczęcia ruchu
        self.migaj = False               # True – krab dopiero się pojawia
        self.ogluszony = False           # True – krab zatrzymany przez pieska

    def aktywny(self):
        return self.czekaj <= 0

    def idz(self, nx, ny):
        self.kierunek = (nx - self.x, ny - self.y)
        self.px, self.py = self.x, self.y
        self.x, self.y = nx, ny
        self.postep = 0.0

    def aktualizuj(self, dt):
        if self.czekaj > 0:
            self.czekaj -= dt
            if self.czekaj <= 0:
                self.migaj = False
                self.ogluszony = False
        if self.postep < 1.0:
            self.postep = min(1.0, self.postep + dt / self.czas_kroku)

    def gotowy(self):
        return self.postep >= 1.0

    def srodek_ekranu(self):
        t = self.postep
        fx = self.px + (self.x - self.px) * t
        fy = self.py + (self.y - self.py) * t
        return fx * KAFEL + KAFEL / 2, fy * KAFEL + KAFEL / 2 + PASEK


def rysuj_zolwia(ekran, zolw, czas):
    cx, cy = zolw.srodek_ekranu()
    dx, dy = zolw.kierunek
    r = KAFEL * 0.36
    # łapki (machają podczas ruchu)
    mach = math.sin(czas * 18) * 2 if not zolw.gotowy() else 0
    px, py = -dy, dx  # wektor prostopadły
    for s, k in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
        lx = cx + dx * r * 0.6 * k + px * r * 0.8 * s + dx * mach * s * k
        ly = cy + dy * r * 0.6 * k + py * r * 0.8 * s + dy * mach * s * k
        pygame.draw.circle(ekran, ZOLW_SKORA, (lx, ly), r * 0.32)
    # głowa
    pygame.draw.circle(ekran, ZOLW_SKORA, (cx + dx * r * 1.05, cy + dy * r * 1.05), r * 0.38)
    oko_x = cx + dx * r * 1.2 + px * r * 0.15
    oko_y = cy + dy * r * 1.2 + py * r * 0.15
    pygame.draw.circle(ekran, (0, 0, 0), (oko_x, oko_y), 2)
    oko_x = cx + dx * r * 1.2 - px * r * 0.15
    oko_y = cy + dy * r * 1.2 - py * r * 0.15
    pygame.draw.circle(ekran, (0, 0, 0), (oko_x, oko_y), 2)
    # skorupa
    pygame.draw.circle(ekran, ZOLW_SKORUPA, (cx, cy), r)
    pygame.draw.circle(ekran, ZOLW_WZOR, (cx, cy), r * 0.45, 2)
    for i in range(6):
        a = i * math.pi / 3
        pygame.draw.line(ekran, ZOLW_WZOR,
                         (cx + math.cos(a) * r * 0.45, cy + math.sin(a) * r * 0.45),
                         (cx + math.cos(a) * r * 0.95, cy + math.sin(a) * r * 0.95), 2)


def rysuj_pieska(ekran, cx, cy, r, czas=0.0, szary=False):
    """Piesek podobny do Yorka (widok z boku, pyszczkiem w prawo); r ~ promień postaci."""
    def k(kolor):
        if not szary:
            return kolor
        sz = sum(kolor) // 3
        return (sz, sz, sz)
    merdanie = math.sin(czas * 20) * r * 0.25
    # ogonek
    pygame.draw.line(ekran, k(YORK_SIERSC), (cx - r * 0.75, cy - r * 0.1),
                     (cx - r * 1.05, cy - r * 0.65 + merdanie * 0.3), max(2, int(r * 0.18)))
    # łapki
    for lx in (-0.55, -0.25, 0.25, 0.5):
        pygame.draw.rect(ekran, k(YORK_PODPALANE),
                         (cx + lx * r - r * 0.1, cy + r * 0.15, r * 0.2, r * 0.45), border_radius=2)
    # tułów z długą, opadającą sierścią (frędzle prawie do ziemi)
    pygame.draw.ellipse(ekran, k(YORK_SIERSC), (cx - r * 0.85, cy - r * 0.4, r * 1.55, r * 0.8))
    fredzle = [(cx - r * 0.8, cy)]
    for i in range(7):
        x = cx - r * 0.8 + i * r * 0.22
        fredzle += [(x + r * 0.05, cy + r * 0.5), (x + r * 0.11, cy + r * 0.3)]
    fredzle.append((cx + r * 0.65, cy))
    pygame.draw.polygon(ekran, k(YORK_SIERSC), fredzle)
    # grzywka opadająca z głowy na grzbiet
    pygame.draw.ellipse(ekran, k(YORK_PODPALANE), (cx + r * 0.2, cy - r * 0.45, r * 0.5, r * 0.55))
    # głowa
    gx, gy = cx + r * 0.65, cy - r * 0.45
    pygame.draw.circle(ekran, k(YORK_PODPALANE), (gx, gy), r * 0.42)
    pygame.draw.ellipse(ekran, k(YORK_PODPALANE), (gx, gy - r * 0.05, r * 0.5, r * 0.3))  # pyszczek
    # spiczaste uszy
    for ux in (-0.25, 0.12):
        pygame.draw.polygon(ekran, k(YORK_PODPALANE), [
            (gx + ux * r - r * 0.12, gy - r * 0.25),
            (gx + ux * r + r * 0.12, gy - r * 0.25),
            (gx + ux * r, gy - r * 0.75)])
    # kokardka
    pygame.draw.circle(ekran, k(YORK_KOKARDA), (gx - r * 0.05, gy - r * 0.4), max(2, r * 0.12))
    # oko i nosek
    pygame.draw.circle(ekran, (0, 0, 0), (gx + r * 0.15, gy - r * 0.08), max(1, r * 0.08))
    pygame.draw.circle(ekran, (0, 0, 0), (gx + r * 0.5, gy + r * 0.08), max(1, r * 0.09))


def rysuj_gwiazdki(ekran, cx, cy, czas):
    """Wirujące gwiazdki nad zatrzymanym krabem."""
    for i in range(3):
        a = czas * 5 + i * 2 * math.pi / 3
        x, y = cx + math.cos(a) * KAFEL * 0.35, cy - KAFEL * 0.45 + math.sin(a) * KAFEL * 0.1
        pygame.draw.circle(ekran, (255, 220, 60), (x, y), 3)


def rysuj_kraba(ekran, krab, czas):
    if krab.migaj and int(krab.czekaj * 8) % 2:
        return  # miganie przy pojawianiu się
    cx, cy = krab.srodek_ekranu()
    r = KAFEL * 0.3
    ruch = math.sin(czas * 14) * 2
    # nóżki
    for s in (-1, 1):
        for i in range(3):
            y0 = cy - r * 0.4 + i * r * 0.4
            pygame.draw.line(ekran, KRAB_CIEMNY, (cx + s * r * 0.8, y0),
                             (cx + s * r * 1.45, y0 + r * 0.35 + (ruch if i % 2 else -ruch)), 3)
    # szczypce
    for s in (-1, 1):
        sx, sy = cx + s * r * 1.0, cy - r * 1.05
        pygame.draw.line(ekran, KRAB_CIEMNY, (cx + s * r * 0.5, cy - r * 0.5), (sx, sy), 3)
        pygame.draw.circle(ekran, KRAB, (sx, sy), r * 0.42)
        pygame.draw.circle(ekran, PODLOGA, (sx, sy - r * 0.25), r * 0.17)
    # tułów
    pygame.draw.ellipse(ekran, KRAB, (cx - r, cy - r * 0.7, r * 2, r * 1.5))
    pygame.draw.ellipse(ekran, KRAB_CIEMNY, (cx - r, cy - r * 0.7, r * 2, r * 1.5), 2)
    # oczy na słupkach
    for s in (-1, 1):
        pygame.draw.line(ekran, KRAB_CIEMNY, (cx + s * r * 0.3, cy - r * 0.5),
                         (cx + s * r * 0.35, cy - r * 0.9), 2)
        pygame.draw.circle(ekran, (255, 255, 255), (cx + s * r * 0.35, cy - r * 0.95), 3)
        pygame.draw.circle(ekran, (0, 0, 0), (cx + s * r * 0.35, cy - r * 0.95), 1)
    if krab.ogluszony:
        rysuj_gwiazdki(ekran, cx, cy, czas)


# ---------------------------------------------------------------------------
# Gra
# ---------------------------------------------------------------------------
class Gra:
    def __init__(self):
        pygame.init()
        ustaw_ikone()
        pygame.display.set_caption(f"{NAZWA} v{WERSJA}")
        self.plansza = pygame.Surface((SZER, WYS))   # gra rysuje się tu, potem skalujemy
        self.pelny_ekran = True
        self.ustaw_tryb()
        self.zegar = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 22, bold=True)
        self.font_maly = pygame.font.SysFont("arial", 16)
        self.font_tytul = pygame.font.SysFont("arial", 72, bold=True)
        self.pomoc = False           # True – widoczna klawiszologia (gra wstrzymana)
        self.font_duzy = pygame.font.SysFont("arial", 56, bold=True)
        self.nowa_gra()

    def ustaw_tryb(self):
        if self.pelny_ekran:
            self.okno = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.okno = pygame.display.set_mode((SZER, WYS))
        pygame.mouse.set_visible(not self.pelny_ekran)

    def przelacz_tryb(self, pelny):
        if pelny != self.pelny_ekran:
            self.pelny_ekran = pelny
            self.ustaw_tryb()

    def nowa_gra(self, poziom=1):
        self.poziom = poziom
        self.krok_kraba = wartosc_poziomu(KROK_KRABA, poziom)
        self.nowy_krab_co = wartosc_poziomu(NOWY_KRAB_CO, poziom)
        start_kraba = wartosc_poziomu(START_KRABA, poziom)
        self.siatka, self.wyjscie = generuj_labirynt(
            KOLUMNY, WIERSZE, wartosc_poziomu(PRZEJSCIA, poziom))
        start = (1, 1)
        self.zolw = Postac(*start, KROK_ZOLWIA)
        # Krab startuje daleko od żółwia, ale nie przy samym wyjściu
        _, odl = najdalsze_pole(self.siatka, start)
        _, odl_wyj = najdalsze_pole(self.siatka, self.wyjscie)
        def ocena(p):
            # daleko po ścieżce i w linii prostej od żółwia, z dala od wyjścia
            prosto = abs(p[0] - start[0]) + abs(p[1] - start[1])
            return min(odl[p], prosto * 1.5, odl_wyj.get(p, 0) * 2)
        pola = [p for p in odl if p != self.wyjscie]
        pole_kraba = max(pola, key=ocena)
        pierwszy = Postac(*pole_kraba, self.krok_kraba)
        pierwszy.czekaj = start_kraba
        self.kraby = [pierwszy]
        self.stan = "start"          # "start", "gra", "wygrana", "przegrana"
        self.czas_gry = 0.0
        self.do_nowego_kraba = self.nowy_krab_co
        self.pieski = []             # pola, na których czekają pieski
        # na wyższych poziomach więcej krabów od początku (ruszają chwilę później)
        for _ in range(min(MAX_KRABOW_START, 1 + (poziom - 1) // KRAB_WIECEJ_CO) - 1):
            self.dodaj_kraba(min_odl=20)
            self.kraby[-1].migaj = False
            self.kraby[-1].czekaj = start_kraba + 1.0
        self.do_pieska = PIESEK_CO   # sekundy do możliwości zostawienia pieska
        self.napisy = []             # [tekst, x, y, pozostały czas] – np. „Hau!”
        self.tlo = self.przygotuj_tlo()

    def przygotuj_tlo(self):
        tlo = pygame.Surface((SZER, WYS))
        tlo.fill(TLO)
        for y, wiersz in enumerate(self.siatka):
            for x, pole in enumerate(wiersz):
                rect = pygame.Rect(x * KAFEL, y * KAFEL + PASEK, KAFEL, KAFEL)
                if pole == SCIANA_T:
                    pygame.draw.rect(tlo, SCIANA, rect)
                    pygame.draw.rect(tlo, SCIANA_JASNA, rect.inflate(-6, -6), border_radius=4)
                else:
                    pygame.draw.rect(tlo, PODLOGA, rect)
        wx, wy = self.wyjscie
        pygame.draw.rect(tlo, WYJSCIE, (wx * KAFEL, wy * KAFEL + PASEK, KAFEL, KAFEL))
        napis = self.font.render("→", True, (255, 255, 255))
        tlo.blit(napis, napis.get_rect(center=(wx * KAFEL + KAFEL / 2, wy * KAFEL + PASEK + KAFEL / 2)))
        return tlo

    # --- logika ---
    def obsluz_zolwia(self):
        if not self.zolw.gotowy():
            return
        klawisze = pygame.key.get_pressed()
        for klawisz, (dx, dy) in KIERUNKI.items():
            if klawisze[klawisz]:
                nx, ny = self.zolw.x + dx, self.zolw.y + dy
                if wolne(self.siatka, nx, ny):
                    self.zolw.idz(nx, ny)
                    return
                self.zolw.kierunek = (dx, dy)

    def obsluz_kraby(self):
        cel = (self.zolw.x, self.zolw.y)
        for krab in self.kraby:
            if not krab.aktywny() or not krab.gotowy():
                continue
            nx, ny = nastepny_krok(self.siatka, (krab.x, krab.y), cel)
            if (nx, ny) != (krab.x, krab.y):
                krab.idz(nx, ny)

    def dodaj_kraba(self, min_odl=MIN_ODLEGLOSC):
        """Nowy krab w losowym wolnym polu, nie za blisko żółwia."""
        _, odl = najdalsze_pole(self.siatka, (self.zolw.x, self.zolw.y))
        zajete = {(k.x, k.y) for k in self.kraby} | {self.wyjscie} | set(self.pieski)
        pola = [p for p, d in odl.items() if d >= min_odl and p not in zajete]
        if not pola:  # awaryjnie: najdalsze wolne pole
            pola = [max((p for p in odl if p not in zajete), key=odl.get)]
        krab = Postac(*random.choice(pola), self.krok_kraba)
        krab.czekaj = POJAWIANIE
        krab.migaj = True
        self.kraby.append(krab)

    def zostaw_pieska(self):
        """Spacja: piesek zostaje na polu za żółwiem (lub pod nim, gdy z tyłu jest ściana)."""
        if self.stan != "gra" or self.do_pieska > 0:
            return
        z = self.zolw
        if not z.gotowy():
            pole = (z.px, z.py)                      # pole, z którego żółw właśnie schodzi
        else:
            dx, dy = z.kierunek
            pole = (z.x - dx, z.y - dy)
            if not wolne(self.siatka, *pole) or pole[0] >= KOLUMNY - 1:
                pole = (z.x, z.y)
        if pole not in self.pieski:
            self.pieski.append(pole)
        self.do_pieska = PIESEK_CO

    def obsluz_pieski(self):
        for krab in self.kraby:
            pole = (krab.x, krab.y)
            if pole in self.pieski and not krab.migaj:
                self.pieski.remove(pole)
                krab.czekaj = ZATRZYMANIE
                krab.ogluszony = True
                cx, cy = pole[0] * KAFEL + KAFEL / 2, pole[1] * KAFEL + PASEK
                self.napisy.append(["Hau!", cx, cy, 1.0])

    def zlapany(self, krab):
        # złapanie: ta sama komórka albo mijanie się w przejściu
        z, k = self.zolw, krab
        if k.migaj:
            return False
        return (z.x, z.y) == (k.x, k.y) or \
            ((z.x, z.y) == (k.px, k.py) and (k.x, k.y) == (z.px, z.py)
             and not (z.gotowy() and k.gotowy()))

    def sprawdz_koniec(self):
        if any(self.zlapany(k) for k in self.kraby):
            self.stan = "przegrana"
        elif (self.zolw.x, self.zolw.y) == self.wyjscie and self.zolw.gotowy():
            self.stan = "wygrana"

    def aktualizuj(self, dt):
        if self.stan != "gra" or self.pomoc:
            return
        self.czas_gry += dt
        self.do_nowego_kraba -= dt
        if self.do_nowego_kraba <= 0:
            self.dodaj_kraba()
            self.do_nowego_kraba += self.nowy_krab_co
        self.do_pieska = max(0.0, self.do_pieska - dt)
        for n in self.napisy:
            n[2] -= dt * 25
            n[3] -= dt
        self.napisy = [n for n in self.napisy if n[3] > 0]
        self.zolw.aktualizuj(dt)
        for krab in self.kraby:
            krab.aktualizuj(dt)
        self.obsluz_zolwia()
        self.obsluz_kraby()
        self.obsluz_pieski()
        self.sprawdz_koniec()

    # --- rysowanie ---
    def rysuj(self):
        ekran = self.plansza
        ekran.blit(self.tlo, (0, 0))
        for px, py in self.pieski:
            rysuj_pieska(ekran, px * KAFEL + KAFEL / 2, py * KAFEL + PASEK + KAFEL * 0.6,
                         KAFEL * 0.42, self.czas_gry)
        rysuj_zolwia(ekran, self.zolw, self.czas_gry)
        for krab in self.kraby:
            rysuj_kraba(ekran, krab, self.czas_gry)
        for tekst, x, y, _ in self.napisy:
            n = self.font.render(tekst, True, (120, 60, 20))
            ekran.blit(n, n.get_rect(center=(x, y)))
        self.rysuj_ikone_pieska(ekran)

        info = (f"{NAZWA} v{WERSJA}   Poziom: {self.poziom}   Czas: {self.czas_gry:5.1f} s   "
                f"Kraby: {len(self.kraby)}   Nowy krab za: {math.ceil(self.do_nowego_kraba):2d} s")
        ekran.blit(self.font.render(info, True, TEKST), (10, 6))
        pomoc = self.font_maly.render(
            "Strzałki/WASD – ruch   Spacja – piesek   K – klawiszologia", True, (170, 175, 190))
        ekran.blit(pomoc, (10, 36))

        if self.pomoc:
            self.przyciemnij(ekran)
            self.rysuj_klawiszologie(ekran)
        elif self.stan == "start":
            self.przyciemnij(ekran)
            self.rysuj_ekran_startowy(ekran)
        elif self.stan != "gra":
            self.przyciemnij(ekran)
            if self.stan == "wygrana":
                tekst, kolor = f"POZIOM {self.poziom} UKOŃCZONY!", (120, 230, 120)
                dalej = f"Enter – przejdź do poziomu {self.poziom + 1}"
            else:
                tekst, kolor = "PRZEGRANA! Krab złapał żółwika!", (240, 100, 90)
                dalej = f"Enter – spróbuj jeszcze raz poziom {self.poziom}"
            n1 = self.font_duzy.render(tekst, True, kolor)
            n2 = self.font.render(f"Czas: {self.czas_gry:.1f} s,  kraby: {len(self.kraby)}", True, TEKST)
            n3 = self.font.render(dalej, True, (255, 220, 90))
            n4 = self.font.render("P – nowa gra od poziomu 1     K – klawiszologia", True, TEKST)
            ekran.blit(n1, n1.get_rect(center=(SZER / 2, WYS / 2 - 40)))
            ekran.blit(n2, n2.get_rect(center=(SZER / 2, WYS / 2 + 20)))
            ekran.blit(n3, n3.get_rect(center=(SZER / 2, WYS / 2 + 60)))
            ekran.blit(n4, n4.get_rect(center=(SZER / 2, WYS / 2 + 95)))
        self.pokaz()

    def przyciemnij(self, ekran):
        zaslona = pygame.Surface((SZER, WYS), pygame.SRCALPHA)
        zaslona.fill((0, 0, 0, 160))
        ekran.blit(zaslona, (0, 0))

    def rysuj_ramke(self, ekran, w, h):
        ramka = pygame.Rect(0, 0, w, h)
        ramka.center = (SZER / 2, PASEK + (WYS - PASEK) / 2)
        pygame.draw.rect(ekran, (30, 36, 52), ramka, border_radius=16)
        pygame.draw.rect(ekran, SCIANA_JASNA, ramka, 3, border_radius=16)
        return ramka

    def rysuj_ekran_startowy(self, ekran):
        ramka = self.rysuj_ramke(ekran, 760, 470)
        y = ramka.top + 25
        tytul = self.font_tytul.render(NAZWA, True, (120, 230, 120))
        ekran.blit(tytul, tytul.get_rect(midtop=(SZER / 2, y)))
        y += 85
        n = self.font_duzy.render(f"Poziom {self.poziom}", True, (255, 220, 90))
        ekran.blit(n, n.get_rect(midtop=(SZER / 2, y)))
        y += 75
        for linia, kolor in (
                ("Twoje zadanie: pomóż żółwikowi uciec z labiryntu!", TEKST),
                ("Steruj klawiszami W A S D lub strzałkami.", TEKST),
                (f"Uważaj na kraby – co {liczba(self.nowy_krab_co)} s pojawia się nowy.", (240, 150, 140)),
                ("Po 20 sekundach możesz zostawić pieska (Spacja), który zatrzyma kraba.", (205, 175, 120))):
            n = (self.font if kolor == TEKST else self.font_maly).render(linia, True, kolor)
            ekran.blit(n, n.get_rect(midtop=(SZER / 2, y)))
            y += 36
        y += 14
        n = self.font.render("K – klawisze sterujące grą", True, (255, 220, 90))
        ekran.blit(n, n.get_rect(midtop=(SZER / 2, y)))
        y += 50
        if int(pygame.time.get_ticks() / 500) % 2 == 0:
            n = self.font.render("Naciśnij klawisz ruchu, Enter lub Spację, aby zacząć", True, TEKST)
            ekran.blit(n, n.get_rect(midtop=(SZER / 2, y)))

    def rysuj_klawiszologie(self, ekran):
        ramka = self.rysuj_ramke(ekran, 840, 440)
        y = ramka.top + 25
        n = self.font_duzy.render("Klawiszologia", True, (255, 220, 90))
        ekran.blit(n, n.get_rect(midtop=(SZER / 2, y)))
        y += 85
        for klawisz, opis in KLAWISZOLOGIA:
            k = self.font.render(klawisz, True, (255, 220, 90))
            o = self.font.render(opis, True, TEKST)
            ekran.blit(k, k.get_rect(topright=(ramka.left + 260, y)))
            ekran.blit(self.font.render("–", True, TEKST), (ramka.left + 275, y))
            ekran.blit(o, (ramka.left + 300, y))
            y += 38
        y += 10
        n = self.font_maly.render("K lub Esc – zamknij (gra jest wstrzymana)", True, (170, 175, 190))
        ekran.blit(n, n.get_rect(midtop=(SZER / 2, y)))

    def rysuj_ikone_pieska(self, ekran):
        """Ikona pieska na pasku: miga, gdy można go zostawić; szara z odliczaniem, gdy nie."""
        cx, cy = SZER - 150, PASEK / 2 + 4
        if self.do_pieska <= 0:
            if self.stan != "gra" or int(self.czas_gry * 3) % 2 == 0:
                rysuj_pieska(ekran, cx, cy, 20, self.czas_gry)
            napis = self.font.render("SPACJA!", True, (255, 220, 90))
        else:
            rysuj_pieska(ekran, cx, cy, 20, szary=True)
            napis = self.font.render(f"za {math.ceil(self.do_pieska):2d} s", True, (150, 150, 160))
        ekran.blit(napis, napis.get_rect(midleft=(cx + 32, PASEK / 2)))

    def pokaz(self):
        """Przenosi planszę na ekran; w pełnym ekranie skaluje z zachowaniem proporcji."""
        ow, oh = self.okno.get_size()
        if (ow, oh) == (SZER, WYS):
            self.okno.blit(self.plansza, (0, 0))
        else:
            skala = min(ow / SZER, oh / WYS)
            w, h = int(SZER * skala), int(WYS * skala)
            self.okno.fill((0, 0, 0))
            self.okno.blit(pygame.transform.smoothscale(self.plansza, (w, h)),
                           ((ow - w) // 2, (oh - h) // 2))
        pygame.display.flip()

    def obsluz_klawisz(self, klawisz):
        """Zwraca False, gdy gra ma się zakończyć."""
        if klawisz == pygame.K_ESCAPE:
            if self.pomoc:
                self.pomoc = False
            elif self.pelny_ekran:
                self.przelacz_tryb(False)
            else:
                return False
        elif klawisz == pygame.K_k:
            self.pomoc = not self.pomoc
        elif klawisz == pygame.K_F11:
            self.przelacz_tryb(not self.pelny_ekran)
        elif self.pomoc:
            return True                      # przy otwartej klawiszologii reszta nie działa
        elif klawisz == pygame.K_p:
            self.nowa_gra()
        elif self.stan == "start":
            if klawisz in KIERUNKI or klawisz in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                self.stan = "gra"
        elif self.stan in ("wygrana", "przegrana"):
            if klawisz in (pygame.K_RETURN, pygame.K_KP_ENTER):
                nastepny = self.poziom + 1 if self.stan == "wygrana" else self.poziom
                self.nowa_gra(nastepny)
        elif klawisz == pygame.K_SPACE:
            self.zostaw_pieska()
        return True

    def uruchom(self):
        while True:
            dt = self.zegar.tick(FPS) / 1000
            for zd in pygame.event.get():
                if zd.type == pygame.QUIT:
                    return
                if zd.type == pygame.KEYDOWN:
                    if self.obsluz_klawisz(zd.key) is False:
                        return
            self.aktualizuj(dt)
            self.rysuj()


def main():
    try:
        Gra().uruchom()
    finally:
        pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
