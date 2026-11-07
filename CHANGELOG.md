# Historia zmian

Wszystkie istotne zmiany w projekcie **LabiryntOL** są opisywane w tym pliku.

Format oparty jest na [Keep a Changelog](https://keepachangelog.com/pl/1.1.0/).

## [Niewydane]

_Brak zmian._

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
