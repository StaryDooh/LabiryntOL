# Historia zmian

Wszystkie istotne zmiany w projekcie **LabiryntOL** są opisywane w tym pliku.

Format oparty jest na [Keep a Changelog](https://keepachangelog.com/pl/1.1.0/).

## [Niewydane]

_Brak zmian._

## [1.1.0.0] – 2026-11-08

### Dodano
- Ekran startowy z opisem zadania: ucieczka z labiryntu klawiszami WASD lub strzałkami. Gra zaczyna się po naciśnięciu klawisza ruchu, Entera lub Spacji, a do tego czasu czas stoi.
- Na ekranie startowym jest informacja, że klawisz `K` pokazuje klawisze sterujące grą.
- Klawiszologia: klawisz `K` pokazuje i ukrywa listę klawiszy sterujących. Gdy jest widoczna, gra jest wstrzymana. Można ją też zamknąć klawiszem `Esc`.

### Zmieniono
- Nowa gra uruchamia się klawiszem `P` zamiast `R`, który łatwo było wcisnąć niechcący obok `WASD`. Nowa gra zaczyna się od ekranu startowego.
- Pasek informacyjny pokazuje skrót sterowania i podpowiedź „K – klawiszologia”.

## [1.0.0.0] – 2026-11-08

Pierwsza pełna wersja gry.

### Dodano
- Piesek podobny do Yorka. Po 20 sekundach gry można go zostawić za żółwikiem klawiszem `Spacja`. Kolejnego pieska można zostawić co 20 sekund.
- Krab, który wejdzie na pieska, zatrzymuje się na 3 sekundy (nad krabem wirują gwiazdki), a piesek znika z napisem „Hau!”.
- Ikona pieska na pasku informacyjnym. Miga z napisem „SPACJA!”, gdy pieska można zostawić. W przeciwnym razie jest szara i pokazuje, ile sekund zostało.

## [0.0.0.2] – 2026-11-08

### Dodano
- Co 15 sekund w losowym miejscu labiryntu pojawia się nowy krab. Nie pojawia się bliżej niż 8 kroków od żółwika ani na wyjściu.
- Nowy krab przez 1 sekundę miga i jest wtedy niegroźny, potem rusza w pościg.
- Na pasku informacyjnym widać liczbę krabów i czas do pojawienia się następnego.
- Ekran końca gry pokazuje czas gry i liczbę krabów.
- Klawisz `F11` przełącza między pełnym ekranem a oknem.

### Zmieniono
- Gra uruchamia się w trybie pełnoekranowym. Plansza jest skalowana do rozdzielczości ekranu z zachowaniem proporcji, a kursor myszy jest ukryty.
- `Esc` w trybie pełnoekranowym przełącza grę do okna. Dopiero w oknie `Esc` zamyka grę.
- Pasek informacyjny ma dwie linie, w drugiej jest opis sterowania.

## [0.0.0.1] – 2026-11-07

Pierwsza, testowa wersja gry.

### Dodano
- Losowo generowany labirynt (algorytm DFS) z dodatkowymi przejściami tworzącymi pętle.
- Wyjście z labiryntu na prawej krawędzi planszy.
- Żółwik sterowany klawiszami strzałek lub WASD, z płynną animacją ruchu.
- Krab ścigający żółwika najkrótszą drogą (BFS), ruszający 1,5 s po starcie.
- Wybór pola startowego kraba z dala od żółwika i od wyjścia.
- Wygrana po dotarciu do wyjścia i przegrana po złapaniu przez kraba, z ekranem końca gry.
- Nowa gra klawiszem `R` i wyjście klawiszem `Esc`.
- Pasek informacyjny z nazwą i wersją gry, czasem rozgrywki oraz sterowaniem.
- Grafika postaci rysowana kodem, bez zewnętrznych plików.
- Ikona gry `ikona.ico` w pliku .exe i na pasku okna (obsługa ikon z obrazkami PNG i BMP).
- Skrypt `kompiluj.bat` kompilujący grę PyInstallerem w trybie katalogu.
- Plik `Wersja.txt` z informacjami o wersji widocznymi we właściwościach pliku .exe.
- Skrypt instalatora Inno Setup `LabiryntOL.iss`. Tworzy plik `GitHub\Setup_LabiryntOL_<wersja>.exe`, a wersję odczytuje z pliku .exe.
- Plik licencji `LICENCJA.txt`, `README.md` i `CHANGELOG.md`.
