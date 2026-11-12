# 🐢 LabiryntOL

**Wersja:** 1.1.0.0
**Autorzy:** Aleksander Markowski, Krzysztof Markowski

Prosta gra zręcznościowa w Pythonie. Pomóż żółwikowi uciec z labiryntu, zanim złapie go krab! 🦀

Labirynt widać z góry. Przy każdej grze jest losowany na nowo, więc żadna rozgrywka nie wygląda tak samo. Gra uruchamia się w trybie pełnoekranowym.

---

## 🎮 Zasady gry

- Po uruchomieniu gry pojawia się ekran startowy. Grę zaczynasz klawiszem ruchu, Enterem lub Spacją.
- Sterujesz **żółwikiem**, który zaczyna w lewym górnym rogu labiryntu.
- Twoim celem jest dotarcie do **wyjścia**, czyli zielonego pola ze strzałką na prawej krawędzi.
- Po labiryncie biega **krab**. Rusza po chwili od startu i zawsze wybiera najkrótszą drogę do żółwika.
- **Co 15 sekund** w losowym miejscu pojawia się **kolejny krab**. Przez pierwszą sekundę miga i jest niegroźny, a potem też rusza w pościg. Im dłużej zwlekasz, tym trudniej!
- Na pomoc przychodzi **piesek** 🐕 podobny do Yorka. Po 20 sekundach gry możesz go zostawić **spacją** za żółwikiem. Krab, który wpadnie na pieska, **zatrzymuje się na 3 sekundy**, a piesek znika. Kolejnego pieska możesz zostawić co 20 sekund. Gdy piesek jest gotowy, jego ikonka na górze ekranu miga.
- **Wygrywasz**, gdy żółwik dotrze do wyjścia.
- **Przegrywasz**, gdy którykolwiek krab złapie żółwika.

Krab jest wolniejszy od żółwika, a w labiryncie są pętle, więc da się go okrążyć.

## ⌨️ Sterowanie

| Klawisz            | Akcja                          |
|--------------------|--------------------------------|
| `↑` `↓` `←` `→`    | ruch żółwika                   |
| `W` `A` `S` `D`    | ruch żółwika (alternatywnie)   |
| `Spacja`           | zostaw pieska (co 20 s)        |
| `P`                | nowa gra (nowy labirynt)       |
| `K`                | klawiszologia: lista klawiszy, gra wstrzymana |
| `F11`              | pełny ekran / okno             |
| `Esc`              | zamyka klawiszologię; wyjście z pełnego ekranu do okna; w oknie zamyka grę |


## 📜 Licencja

Gra jest **darmowa** i udostępniana „tak jak jest”, bez żadnych gwarancji. Autorzy nie ponoszą odpowiedzialności za skutki jej używania.

Bez pisemnej zgody autorów **nie wolno** gry sprzedawać, przerabiać ani rozpowszechniać jej zmienionych wersji.

Pełna treść licencji znajduje się w pliku [LICENCJA.txt](LICENCJA.txt).

© 2026 Aleksander Markowski, Krzysztof Markowski
