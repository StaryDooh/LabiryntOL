# 🐢 LabiryntOL
 
**Wersja:** 1.2.0.1
**Autorzy:** Aleksander Markowski, Krzysztof Markowski
 
Prosta gra zręcznościowa dla całej rodziny. Pomóż żółwikowi uciec z labiryntu, zanim złapie go krab! 🦀
 
Labirynt widać z góry. Przy każdej grze jest losowany na nowo, więc żadna rozgrywka nie wygląda tak samo. Kolejne poziomy są coraz trudniejsze, a w opałach pomaga wierny piesek.
 
---
 
## 💾 Pobieranie i instalacja
 
1. Pobierz instalator **`Setup_LabiryntOL_<wersja>.exe`** z folderu [GitHub](GitHub/) w tym repozytorium. Wybierz plik o najwyższym numerze wersji.
2. Uruchom pobrany plik i postępuj zgodnie z instrukcjami instalatora:
   - zaakceptuj licencję,
   - wybierz, czy grę zainstalować dla wszystkich użytkowników komputera, czy tylko dla siebie,
   - opcjonalnie zaznacz utworzenie skrótu na pulpicie.
3. Po instalacji grę uruchomisz z **menu Start** (LabiryntOL) albo skrótem na pulpicie.
> **Komunikat „System Windows ochronił komputer”?**
> Instalator nie ma podpisu cyfrowego, więc filtr SmartScreen może wyświetlić ostrzeżenie. Kliknij **Więcej informacji**, a potem **Uruchom mimo to**.
 
**Aktualizacja:** pobierz i uruchom nowszy instalator. Zastąpi poprzednią wersję gry.
 
**Odinstalowanie:** w menu Start wybierz **LabiryntOL → Odinstaluj LabiryntOL**. Możesz też skorzystać z *Ustawienia → Aplikacje → Zainstalowane aplikacje*.
 
### Wymagania
 
- Windows 10 lub 11 (64-bitowy)
- klawiatura 🙂
---
 
## 🎮 Zasady gry
 
- Po uruchomieniu gry pojawia się ekran startowy. Grę zaczynasz klawiszem ruchu, `Enter` lub `Spacją`.
- Sterujesz **żółwikiem**, który zaczyna w lewym górnym rogu labiryntu. Ze startu zawsze wychodzą dwie osobne drogi, więc kraba spotkanego na początku da się obejść.
- Twoim celem jest dotarcie do **wyjścia**, czyli zielonego pola ze strzałką na prawej krawędzi.
- Po labiryncie biega **krab**. Rusza chwilę po starcie i zawsze wybiera najkrótszą drogę do żółwika.
- Co jakiś czas (na poziomie 1 **co 20 sekund**) w losowym miejscu pojawia się **kolejny krab**. Przez pierwszą sekundę miga i jest niegroźny, a potem też rusza w pościg. Im dłużej zwlekasz, tym trudniej!
- Na pomoc przychodzi **piesek** 🐕 podobny do Yorka. Po 20 sekundach gry możesz go zostawić **spacją** za żółwikiem. Krab, który wpadnie na pieska, **zatrzymuje się na 3 sekundy**, a piesek znika. Kolejnego pieska możesz zostawić co 20 sekund. Gdy piesek jest gotowy, jego ikonka w prawym górnym rogu ekranu miga.
- **Wygrywasz poziom**, gdy żółwik dotrze do wyjścia. `Enter` przenosi Cię wtedy do następnego poziomu.
- **Przegrywasz**, gdy którykolwiek krab złapie żółwika. `Enter` pozwala powtórzyć ten sam poziom, a `P` zaczyna grę od poziomu 1.
### 📈 Poziomy trudności
 
Pierwszy poziom jest spokojny, a każdy kolejny jest trochę trudniejszy:
 
| Poziom | Szybkość krabów  | Nowy krab co | Kraby na starcie |
|-------:|------------------|-------------:|-----------------:|
| 1      | wolne            | 20 s         | 1                |
| 3      | trochę szybsze   | 17 s         | 1                |
| 5      | średnie          | 14 s         | 2                |
| 8      | szybkie          | 10 s         | 2                |
| 9+     | najszybsze       | 10 s         | 3                |
 
Z każdym poziomem pierwszy krab rusza też wcześniej, a w labiryncie jest mniej przejść na skróty.
 
### 💡 Wskazówki
 
- Żółwik jest szybszy od krabów. Szukaj w labiryncie pętli, którymi można kraba okrążyć.
- Zostawiaj pieska w wąskim korytarzu tuż przed goniącym Cię krabem. Wtedy na pewno na niego wpadnie.
- Nie zwlekaj! Każdy kolejny krab utrudnia ucieczkę.
- Zgubiłeś się? Klawisz `K` wstrzymuje grę i pokazuje listę klawiszy.
---
 
## ⌨️ Sterowanie
 
| Klawisz                     | Akcja                                                   |
|-----------------------------|---------------------------------------------------------|
| `↑` `↓` `←` `→` lub `W` `A` `S` `D` | ruch żółwika                                    |
| `Spacja`                    | zostaw pieska (co 20 s)                                 |
| `Enter`                     | start / następny poziom / powtórzenie poziomu           |
| `P`                         | nowa gra od poziomu 1                                   |
| `K`                         | klawiszologia: lista klawiszy, gra wstrzymana           |
| `F11`                       | pełny ekran / okno                                      |
| `Esc`                       | zamyka klawiszologię; z pełnego ekranu przełącza do okna; w oknie zamyka grę |
 
Gra uruchamia się na **pełnym ekranie**. Aby z niej wyjść, naciśnij `Esc` dwa razy: pierwsze naciśnięcie przełącza grę do okna, drugie ją zamyka.
 
---
 
## ℹ️ O grze
 
Gra została napisana w języku Python z użyciem biblioteki Pygame. Cała grafika jest rysowana przez program, bez gotowych obrazków.
 
Historię zmian w kolejnych wersjach znajdziesz w pliku [CHANGELOG.md](CHANGELOG.md).
 
## 📜 Licencja
 
Gra jest **darmowa** i udostępniana „tak jak jest”, bez żadnych gwarancji. Autorzy nie ponoszą odpowiedzialności za skutki jej używania.
 
Bez pisemnej zgody autorów **nie wolno** gry sprzedawać, przerabiać ani rozpowszechniać jej zmienionych wersji.
 
Pełna treść licencji znajduje się w pliku [LICENCJA.txt](LICENCJA.txt).
 
© 2026 Aleksander Markowski, Krzysztof Markowski
 