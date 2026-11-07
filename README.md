# 🐢 LabiryntOL

**Wersja:** 0.0.0.1 (wersja testowa)
**Autorzy:** Aleksander Markowski, Krzysztof Markowski

Prosta gra zręcznościowa w Pythonie. Pomóż żółwikowi uciec z labiryntu, zanim złapie go krab! 🦀

Labirynt widać z góry. Przy każdej grze jest losowany na nowo, więc żadna rozgrywka nie wygląda tak samo.

---

## 🎮 Zasady gry

- Sterujesz **żółwikiem**, który zaczyna w lewym górnym rogu labiryntu.
- Twoim celem jest dotarcie do **wyjścia**, czyli zielonego pola ze strzałką na prawej krawędzi.
- Po labiryncie biega **krab**. Rusza po chwili od startu i zawsze wybiera najkrótszą drogę do żółwika.
- **Wygrywasz**, gdy żółwik dotrze do wyjścia.
- **Przegrywasz**, gdy krab złapie żółwika.

Krab jest wolniejszy od żółwika, a w labiryncie są pętle, więc da się go okrążyć.

## ⌨️ Sterowanie

| Klawisz            | Akcja                          |
|--------------------|--------------------------------|
| `↑` `↓` `←` `→`    | ruch żółwika                   |
| `W` `A` `S` `D`    | ruch żółwika (alternatywnie)   |
| `R`                | nowa gra (nowy labirynt)       |
| `Esc`              | wyjście z gry                  |

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

Instalator powstaje w podkatalogu `GitHub`, np. `GitHub\Setup_LabiryntOL_0.0.0.1.exe`. Numer wersji jest odczytywany automatycznie z pliku `LabiryntOL.exe`, więc w skrypcie Inno Setup nie trzeba go zmieniać.

Instalator jest w języku polskim i wyświetla licencję. Tworzy skrót w menu Start, a skrót na pulpicie opcjonalnie. Pozwala zainstalować grę dla wszystkich użytkowników albo tylko dla bieżącego.

## ⚙️ Dostosowanie gry

Na początku pliku `labiryntol.py` znajdują się stałe, które zmieniają rozgrywkę:

| Stała                   | Opis                                                  | Domyślnie |
|-------------------------|-------------------------------------------------------|-----------|
| `KOLUMNY`, `WIERSZE`    | rozmiar labiryntu w kaflach (liczby nieparzyste)      | 31 × 21   |
| `KAFEL`                 | rozmiar jednego kafla w pikselach                     | 32        |
| `KROK_ZOLWIA`           | czas jednego kroku żółwia (s), mniej oznacza szybciej | 0.13      |
| `KROK_KRABA`            | czas jednego kroku kraba (s), mniej oznacza szybciej  | 0.24      |
| `START_KRABA`           | po ilu sekundach krab rusza w pościg                  | 1.5       |
| `DODATKOWE_PRZEJSCIA`   | część usuwanych ścian (więcej pętli, łatwiejsza gra)  | 0.08      |

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
