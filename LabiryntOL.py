"""
LabiryntOL - prosta gra labiryntowa (wersja testowa)
Żółwik ucieka z labiryntu, krab próbuje go złapać.

Sterowanie: strzałki lub WASD
R - nowa gra, Esc - wyjście

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
WERSJA = "0.0.0.1"

KOLUMNY = 31          # liczba kafli w poziomie (nieparzysta)
WIERSZE = 21          # liczba kafli w pionie (nieparzysta)
KAFEL = 32            # rozmiar kafla w pikselach
PASEK = 40            # wysokość paska informacyjnego u góry
FPS = 60

KROK_ZOLWIA = 0.13    # sekundy na jeden krok żółwia (przy wciśniętym klawiszu)
KROK_KRABA = 0.24     # sekundy na jeden krok kraba
START_KRABA = 1.5     # krab rusza po tylu sekundach
DODATKOWE_PRZEJSCIA = 0.08  # część ścian usuwanych, by powstały pętle

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

SCIANA_T, PUSTE_T = 1, 0

KIERUNKI = {
    pygame.K_UP: (0, -1), pygame.K_w: (0, -1),
    pygame.K_DOWN: (0, 1), pygame.K_s: (0, 1),
    pygame.K_LEFT: (-1, 0), pygame.K_a: (-1, 0),
    pygame.K_RIGHT: (1, 0), pygame.K_d: (1, 0),
}


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
def generuj_labirynt(kol, wier):
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
    for x, y in kandydaci[: int(len(kandydaci) * DODATKOWE_PRZEJSCIA)]:
        siatka[y][x] = PUSTE_T

    # Wyjście na prawej krawędzi, w dolnej połowie
    wy = random.choice(range(wier // 2 | 1, wier - 1, 2))
    siatka[wy][kol - 1] = PUSTE_T
    return siatka, (kol - 1, wy)


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

    def idz(self, nx, ny):
        self.kierunek = (nx - self.x, ny - self.y)
        self.px, self.py = self.x, self.y
        self.x, self.y = nx, ny
        self.postep = 0.0

    def aktualizuj(self, dt):
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


def rysuj_kraba(ekran, krab, czas):
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


# ---------------------------------------------------------------------------
# Gra
# ---------------------------------------------------------------------------
class Gra:
    def __init__(self):
        pygame.init()
        ustaw_ikone()
        pygame.display.set_caption(f"{NAZWA} v{WERSJA}")
        self.ekran = pygame.display.set_mode((SZER, WYS))
        self.zegar = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 22, bold=True)
        self.font_duzy = pygame.font.SysFont("arial", 56, bold=True)
        self.nowa_gra()

    def nowa_gra(self):
        self.siatka, self.wyjscie = generuj_labirynt(KOLUMNY, WIERSZE)
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
        self.krab = Postac(*pole_kraba, KROK_KRABA)
        self.stan = "gra"            # "gra", "wygrana", "przegrana"
        self.czas_gry = 0.0
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

    def obsluz_kraba(self):
        if self.czas_gry < START_KRABA or not self.krab.gotowy():
            return
        cel = (self.zolw.x, self.zolw.y)
        nx, ny = nastepny_krok(self.siatka, (self.krab.x, self.krab.y), cel)
        if (nx, ny) != (self.krab.x, self.krab.y):
            self.krab.idz(nx, ny)

    def sprawdz_koniec(self):
        # złapanie: ta sama komórka albo mijanie się w przejściu
        z, k = self.zolw, self.krab
        zderzenie = (z.x, z.y) == (k.x, k.y) or \
                    ((z.x, z.y) == (k.px, k.py) and (k.x, k.y) == (z.px, z.py)
                     and not (z.gotowy() and k.gotowy()))
        if zderzenie:
            self.stan = "przegrana"
        elif (z.x, z.y) == self.wyjscie and z.gotowy():
            self.stan = "wygrana"

    def aktualizuj(self, dt):
        if self.stan != "gra":
            return
        self.czas_gry += dt
        self.zolw.aktualizuj(dt)
        self.krab.aktualizuj(dt)
        self.obsluz_zolwia()
        self.obsluz_kraba()
        self.sprawdz_koniec()

    # --- rysowanie ---
    def rysuj(self):
        self.ekran.blit(self.tlo, (0, 0))
        rysuj_zolwia(self.ekran, self.zolw, self.czas_gry)
        rysuj_kraba(self.ekran, self.krab, self.czas_gry)

        info = f"{NAZWA} v{WERSJA}    Czas: {self.czas_gry:5.1f} s    Strzałki/WASD – ruch,  R – nowa gra,  Esc – wyjście"
        self.ekran.blit(self.font.render(info, True, TEKST), (10, 8))

        if self.stan != "gra":
            zaslona = pygame.Surface((SZER, WYS), pygame.SRCALPHA)
            zaslona.fill((0, 0, 0, 150))
            self.ekran.blit(zaslona, (0, 0))
            if self.stan == "wygrana":
                tekst, kolor = "WYGRANA! Żółwik uciekł!", (120, 230, 120)
            else:
                tekst, kolor = "PRZEGRANA! Krab złapał żółwika!", (240, 100, 90)
            n1 = self.font_duzy.render(tekst, True, kolor)
            n2 = self.font.render("R – zagraj ponownie,  Esc – wyjście", True, TEKST)
            self.ekran.blit(n1, n1.get_rect(center=(SZER / 2, WYS / 2 - 20)))
            self.ekran.blit(n2, n2.get_rect(center=(SZER / 2, WYS / 2 + 40)))
        pygame.display.flip()

    def uruchom(self):
        while True:
            dt = self.zegar.tick(FPS) / 1000
            for zd in pygame.event.get():
                if zd.type == pygame.QUIT:
                    return
                if zd.type == pygame.KEYDOWN:
                    if zd.key == pygame.K_ESCAPE:
                        return
                    if zd.key == pygame.K_r:
                        self.nowa_gra()
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
