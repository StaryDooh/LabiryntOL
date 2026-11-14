# 🐢 LabiryntOL

**Wersja:** 1.2.0.1
**Autorzy:** Aleksander Markowski, Krzysztof Markowski

Prosta gra zręcznościowa w Pythonie. Pomóż żółwikowi uciec z labiryntu, zanim złapie go krab! 🦀

Labirynt widać z góry. Przy każdej grze jest losowany na nowo, więc żadna rozgrywka nie wygląda tak samo. Gra uruchamia się w trybie pełnoekranowym.

---

## 🎮 Zasady gry

- Po uruchomieniu gry pojawia się ekran startowy. Grę zaczynasz klawiszem ruchu, Enterem lub Spacją.
- Sterujesz **żółwikiem**, który zaczyna w lewym górnym rogu labiryntu. Ze startu zawsze wychodzą dwie osobne drogi, więc kraba spotkanego na początku da się obejść.
- Twoim celem jest dotarcie do **wyjścia**, czyli zielonego pola ze strzałką na prawej krawędzi.
- Po labiryncie biega **krab**. Rusza po chwili od startu i zawsze wybiera najkrótszą drogę do żółwika.
- Co jakiś czas (na poziomie 1 **co 20 sekund**) w losowym miejscu pojawia się **kolejny krab**. Przez pierwszą sekundę miga i jest niegroźny, a potem też rusza w pościg. Im dłużej zwlekasz, tym trudniej!
- Na pomoc przychodzi **piesek** 🐕 podobny do Yorka. Po 20 sekundach gry możesz go zostawić **spacją** za żółwikiem. Krab, który wpadnie na pieska, **zatrzymuje się na 3 sekundy**, a piesek znika. Kolejnego pieska możesz zostawić co 20 sekund. Gdy piesek jest gotowy, jego ikonka na górze ekranu miga.
- **Wygrywasz poziom**, gdy żółwik dotrze do wyjścia. `Enter` przenosi Cię wtedy do następnego poziomu.
- **Przegrywasz**, gdy którykolwiek krab złapie żółwika. `Enter` pozwala powtórzyć ten sam poziom, a `P` zaczyna grę od poziomu 1.

### 📈 Poziomy trudności

Pierwszy poziom jest spokojny, a każdy kolejny jest trochę trudniejszy:

| Poziom | Krok kraba | Nowy krab co | Kraby na starcie |
|-------:|-----------:|-------------:|-----------------:|
| 1      | 0,32 s     | 20 s         | 1                |
| 3      | 0,29 s     | 17 s         | 1                |
| 5      | 0,26 s     | 14 s         | 2                |
| 8      | 0,215 s    | 10 s         | 2                |
| 9+     | 0,20 s     | 10 s         | 3                |

Z każdym poziomem pierwszy krab rusza też wcześniej, a w labiryncie jest mniej pętli.

Krab jest wolniejszy od żółwika, a w labiryncie są pętle, więc da się go okrążyć.

## ⌨️ Sterowanie

| Klawisz            | Akcja                          |
|--------------------|--------------------------------|
| `↑` `↓` `←` `→`    | ruch żółwika                   |
| `W` `A` `S` `D`    | ruch żółwika (alternatywnie)   |
| `Spacja`           | zostaw pieska (co 20 s)        |
| `Enter`            | start / następny poziom / powtórzenie poziomu |
| `P`                | nowa gra od poziomu 1          |
| `K`                | klawiszologia: lista klawiszy, gra wstrzymana |
| `F11`              | pełny ekran / okno             |
| `Esc`              | zamyka klawiszologię; wyjście z pełnego ekranu do okna; w oknie zamyka grę |

## 📋 Wymagania

- Python 3.9 lub nowszy
- [pygame-ce](https://pypi.org/project/pygame-ce/) (zalecane) lub klasyczny [pygame](https://pypi.org/project/pygame/)

## 🚀 Instalacja i uruchomienie

1. Pobierz repozytorium, np. przyciskiem **Code → Download ZIP** albo poleceniem:
   ```bash
   git clone <adres-repozytorium>
   cd LabiryntOL
   ```
2. Zainstaluj bibliotekę:
   ```bash
   pip install pygame-ce
   ```
3. Uruchom grę:
   ```bash
   python labiryntol.py
   ```

## 📦 Tworzenie pliku .exe (Windows)

Grę kompiluje się za pomocą [PyInstaller](https://pyinstaller.org/) w trybie katalogu (`--onedir`). Wystarczy uruchomić skrypt:

```bat
kompiluj.bat
```

Skrypt:
- sprawdza, czy są wszystkie potrzebne pliki, i w razie potrzeby instaluje PyInstaller,
- usuwa wyniki poprzedniej kompilacji,
- kompiluje grę z ikoną `ikona.ico` i informacjami o wersji z `Wersja.txt`,
- kopiuje do gotowego katalogu `LICENCJA.txt`, `README.md` i `CHANGELOG.md`.

Gotowa gra znajduje się w folderze `dist\LabiryntOL\`. Uruchamia się ją plikiem `LabiryntOL.exe`. Rozpowszechniaj **cały katalog**, a nie sam plik .exe.

> Przy zmianie wersji gry zaktualizuj numer w trzech miejscach: `WERSJA` w `labiryntol.py`, `filevers`/`prodvers` oraz `FileVersion`/`ProductVersion` w `Wersja.txt`.

## 💿 Tworzenie instalatora (Inno Setup)

Do zbudowania instalatora potrzebny jest [Inno Setup 6](https://jrsoftware.org/isinfo.php).

1. Najpierw skompiluj grę skryptem `kompiluj.bat`.
2. Otwórz plik `LabiryntOL.iss` w Inno Setup i wybierz **Build → Compile**. Możesz też skompilować go z wiersza poleceń:
   ```bat
   "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" LabiryntOL.iss
   ```

Instalator powstaje w podkatalogu `GitHub`, np. `GitHub\Setup_LabiryntOL_1.2.0.1.exe`. Numer wersji jest odczytywany automatycznie z pliku `LabiryntOL.exe`, więc w skrypcie Inno Setup nie trzeba go zmieniać.

Instalator jest w języku polskim i wyświetla licencję. Tworzy skrót w menu Start, a skrót na pulpicie opcjonalnie. Pozwala zainstalować grę dla wszystkich użytkowników albo tylko dla bieżącego.

## ⚙️ Dostosowanie gry

Na początku pliku `labiryntol.py` znajdują się stałe, które zmieniają rozgrywkę. Parametry zależne od poziomu mają postać trójki: **(wartość na poziomie 1, zmiana na każdy kolejny poziom, granica)**.

| Stała                   | Opis                                                  | Domyślnie |
|-------------------------|-------------------------------------------------------|-----------|
| `KOLUMNY`, `WIERSZE`    | rozmiar labiryntu w kaflach (liczby nieparzyste)      | 31 × 21   |
| `KAFEL`                 | rozmiar jednego kafla w pikselach                     | 32        |
| `KROK_ZOLWIA`           | czas jednego kroku żółwia (s), mniej oznacza szybciej | 0.13      |
| `KROK_KRABA`            | czas kroku kraba (s), mniej oznacza szybciej          | (0.32, -0.015, 0.20) |
| `START_KRABA`           | po ilu sekundach rusza pierwszy krab                  | (3.0, -0.25, 1.0) |
| `NOWY_KRAB_CO`          | co ile sekund pojawia się nowy krab                   | (20.0, -1.5, 10.0) |
| `PRZEJSCIA`             | część usuwanych ścian (więcej pętli = łatwiej)        | (0.14, -0.01, 0.05) |
| `KRAB_WIECEJ_CO`        | co ile poziomów o jednego kraba więcej na starcie     | 4         |
| `MAX_KRABOW_START`      | najwięcej krabów na starcie poziomu                   | 3         |
| `POJAWIANIE`            | jak długo nowy krab miga, zanim ruszy (s)             | 1.0       |
| `MIN_ODLEGLOSC`         | min. odległość nowego kraba od żółwia (w krokach)     | 8         |
| `ODNOGI_STARTU`         | min. długość dwóch osobnych dróg ze startu (część szerokości planszy) | 1/3 |
| `PIESEK_CO`             | co ile sekund można zostawić pieska                   | 20        |
| `ZATRZYMANIE`           | na ile sekund piesek zatrzymuje kraba                 | 3         |

## 📁 Struktura projektu

```
LabiryntOL/
├── labiryntol.py    # kod gry
├── ikona.ico        # ikona gry (plik .exe i okno)
├── Wersja.txt       # informacje o wersji dla PyInstallera
├── kompiluj.bat     # skrypt kompilujący do .exe
├── LabiryntOL.iss   # skrypt instalatora Inno Setup
├── GitHub/          # gotowe instalatory (Setup_LabiryntOL_<wersja>.exe)
├── README.md        # ten plik
├── CHANGELOG.md     # historia zmian
└── LICENCJA.txt     # licencja
```

## 📜 Licencja

Gra jest **darmowa** i udostępniana „tak jak jest”, bez żadnych gwarancji. Autorzy nie ponoszą odpowiedzialności za skutki jej używania.

Bez pisemnej zgody autorów **nie wolno** gry sprzedawać, przerabiać ani rozpowszechniać jej zmienionych wersji.

Pełna treść licencji znajduje się w pliku [LICENCJA.txt](LICENCJA.txt).

© 2026 Aleksander Markowski, Krzysztof Markowski
