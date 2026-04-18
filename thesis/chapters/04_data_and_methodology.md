# Chapter 4 — Data and Methodology

## 4.1 Korpusy danych

Niniejszy podrozdział opisuje trzy korpusy, na których opiera się empiryczna część pracy, oraz przedstawia argumentację strukturalnych różnic między nimi. Zakresem opisu są: pochodzenie danych i warunki ich udostępnienia, skala surowego zasobu i pokrycie czasowe, schemat analityczny uzyskany po wstępnym czyszczeniu (Phase 01, Pipeline Section 01_04), kompletność cech oraz udokumentowane asymetrie — zarówno wewnątrzkorpusowe (stronnicość slotów, sentyncjalne wartości rankingowe), jak i międzykorpusowe. Nie powtarza się tutaj mechaniki rozgrywki ani charakterystyki scen rywalizacyjnych — te zagadnienia są przedmiotem §2.2 (StarCraft II) oraz §2.3 (Age of Empires II); w tym miejscu ogranicza się odniesienia do §1.4 (zakres i ograniczenia) w części, która ramuje asymetrię „populacja zawodowa vs. populacja rankingowa" jako świadomy wybór metodologiczny. Szczegóły reguł czyszczenia omówione są w §4.2, schemat cech w §4.3, a protokół eksperymentalny operujący na dokumentowanych tutaj ograniczeniach — w §4.4. Konsekwencje wymienionych tu ograniczeń dla trafności wniosków wyciąganych z porównań międzykorpusowych syntetyzuje §6.5.

Zawartość podrozdziału zorganizowana jest wokół trzech korpusów i krzyżowego zestawienia ich charakterystyk. §4.1.1 omawia korpus SC2EGSet [Bialecki2023] dla StarCraft II. §4.1.2 omawia dwa komplementarne korpusy Age of Empires II — aoestats [AoEStats] oraz aoe2companion [AoeCompanion] — dla których w §4.1.2.0 uzasadnia się strategię dwukorpusową. §4.1.3 syntezuje wnioski porównawcze i prezentuje dwie tabele asymetrii (Tabela 4.4a — Skala i akwizycja; Tabela 4.4b — Asymetria analityczna). Wszystkie liczby cytowane w tym podrozdziale pochodzą z artefaktów Phase 01 (sekcje 01_01 do 01_04) odpowiedniego korpusu; artefakty te są jedynym dopuszczalnym źródłem twierdzeń liczbowych, zgodnie z wymogiem wewnętrznej spójności dokumentowanym w niezmiennikach projektu (I7) i zasadą niemodyfikowalności surowych danych (I9).

### 4.1.1 Korpus SC2EGSet (StarCraft II)

#### 4.1.1.0 Cytowanie i pozyskanie

Dane dla StarCraft II pochodzą z korpusu *SC2EGSet: StarCraft II Esport Replay and Game-state Dataset* [Bialecki2023], opublikowanego w czasopiśmie *Scientific Data* i dystrybuowanego za pośrednictwem repozytorium Zenodo (https://zenodo.org/records/17829625) w wersji v2.1.0 [REVIEW: zweryfikować identyfikator wersji z metadanymi Zenodo; numer 17829625 pochodzi z `THESIS_STRUCTURE.md` i wymaga potwierdzenia]. Licencja dystrybucji określona jest jako CC-BY 4.0 [REVIEW: licencja wymaga potwierdzenia bezpośrednio z metadanych Zenodo; w przypadku rozbieżności — zaktualizować atrybucję]. Data pozyskania danych do niniejszej pracy to 2026-04-09 — dzień wykonania kroku 01_01_01 `file_inventory` w trybie produkcyjnym, zgodnie z research_log Phase 01 (plik `reports/research_log.md`, krok 01_01_01) [REVIEW: krok 01_01_01 nie rejestruje explicite daty pozyskania jako pola artefaktu; użyto daty wykonania kroku jako proxy]. W kontekście dostępnych publicznie korpusów SC2 — obejmujących UAlbertaBot Replay Dataset oraz MSC [Wu2017MSC] — SC2EGSet [Bialecki2023] wyróżnia się pełną dystrybucją zdekodowanych plików `.SC2Replay` jako JSON, zawierających nie tylko metadane meczu, lecz także kompletne strumienie zdarzeń trakerowych, zdarzeń wewnątrzgrowych i komunikatów; pełniejsza analiza literaturowa korpusów SC2 znajduje się w §3.2. Decyzja o oparciu predykcji SC2 na korpusie [Bialecki2023], a nie na MSC [Wu2017MSC], wynika z trzech jednoczesnych okoliczności: pełnej dystrybucji plików zdekodowanych strumieni zdarzeń, większej liczby zdarzeń trakerowych na replay dostępnych do ekstrakcji cech (szczegóły w §4.1.1.2) oraz dłuższego okresu temporalnego obejmującego zarówno lata świetności serii WCS, jak i zmianę struktury sceny po 2020 r. (porównanie z MSC — zgodnie z literaturą omawianą w §3.2).

#### 4.1.1.1 Skala i pokrycie czasowe korpusu

Na podstawie inwentarza plików w kroku 01_01_01 można stwierdzić, że korpus obejmuje 70 katalogów turniejowych z lat 2016–2024, łącznie 22 390 plików `.SC2Replay.json` o sumarycznym rozmiarze ~214 GB. Rozkład liczby powtórek w obrębie turnieju jest silnie niesymetryczny — najmniejszy katalog (2016 IEM 10 Taipei) zawiera 30 powtórek, największy (2022_03_DH_SC2_Masters_Atlanta) — 1 296, a mediana liczby powtórek na turniej wynosi 260,5. Asymetria ta wynika ze zróżnicowanych formatów turniejowych (grupowe Bo3, pucharowe Bo5, finały Bo7) oraz wielkości drabinki kwalifikacyjnej — odnotowano ją jako fakt strukturalny, którego konsekwencje dla stratyfikacji temporalnej w protokole walidacji są przedmiotem §4.4.

Pokrycie czasowe, zweryfikowane poprzez pole `details.timeUTC` w kroku 01_02_04 univariate census, rozciąga się od 2016-01-07 do 2024-12-01 i obejmuje 76 odrębnych miesięcy kalendarzowych, z 32 miesiącami o zerowym pokryciu (`01_03_01_systematic_profile.md`). Dystrybucja miesięczna powtórek jest silnie skośna — koncentracja występuje w sezonach 2018–2022, odpowiadających szczytowi programu World Championship Series oraz pierwszym sezonom ESL Pro Tour. Luki w pokryciu miesięcznym odpowiadają przerwom między-turniejowym i okresom, w których w kompletowanym zbiorze nie znalazły się powtórki z wybranych turniejów [REVIEW: szczegółowa stratyfikacja temporalna per-turniej zarezerwowana dla Step 01_05 (Temporal & Panel EDA); §4.1.1 ogranicza się do inwentarzowego pokrycia]. Uwagę zwraca fakt, że decyzja o budowie korpusu wyłącznie turniejowego — w odróżnieniu od losowych próbek rozgrywek rankingowych z Battle.net — jest projektowym wyborem autorów SC2EGSet [Bialecki2023]; konsekwencją jest wąskie pokrycie populacji zawodowej i brak reprezentacji mechaniki automatycznego doboru meczów (ang. *matchmaking*), co dokumentuje się odrębnie w §4.1.1.5. Skala SC2EGSet w kontekście porównawczym wszystkich trzech korpusów przedstawiona jest w Tabeli 4.4a w §4.1.3.

Wybór scope'u prawdziwego 1v1 rozstrzygniętego (ang. *true 1v1 decisive*) jako jedynego zakresu predykcji — w odróżnieniu od wszystkich meczów 1v1, w tym nierozstrzygniętych — wynika bezpośrednio z operacjonalizacji zadania predykcji binarnej omówionej w §1.2. Pozostawienie w zakresie meczów Undecided lub Tie wymagałoby zmiany sformułowania zadania na wielomodalne, co wykracza poza zakres niniejszej pracy (forward reference do §4.4.1).

#### 4.1.1.2 Struktura plików powtórek i strumieni zdarzeń

Pliki `.SC2Replay` w wersji zdekodowanej do formatu JSON rozpadają się na trzy strumienie zdarzeń, których liczności w całym korpusie zostały ustalone w kroku 01_03_04 (Event Profiling). Strumień trakerowy (`tracker_events_raw`) zawiera 62 003 411 zdarzeń reprezentujących 10 typów — od narodzin jednostek (UnitBorn dominujący z udziałem 36,08%) przez śmierć jednostek (UnitDied 25,89%) i zmiany typu (UnitTypeChange 17,74%) po periodyczny typ PlayerStats (7,35%); strumień wewnątrzgrowy (`game_events_raw`) obejmuje 608 618 823 zdarzeń 23 typów, w którym dominuje CameraUpdate (63,67%); strumień komunikatów (`message_events_raw`) obejmuje 52 167 zdarzeń 3 typów, z pokryciem 99,42% powtórek. Typy UnitBorn, PlayerStats i PlayerSetup osiągają pokrycie 100% powtórek, co potwierdza ich strukturalne występowanie w każdym meczu, podczas gdy UnitOwnerChange pokrywa jedynie 25,39% powtórek — odzwierciedla to rzadkość zjawisk typu *Neural Parasite* (mind control) w kompetytywnej praktyce.

Periodyczność zdarzeń PlayerStats — ustalona empirycznie w kroku 01_03_04 — wynosi 160 *game loops* dla zdecydowanej większości obserwacji, co przy nominalnej prędkości *Faster* (22,4 *game loops* na sekundę rzeczywistą, cytowanej za [Liquipedia_GameSpeed] w §2.2.4) przekłada się na interwał ~7,14 s. Ta naturalna kadencja stanowi rytm próbkowania cech śródmeczowych wykorzystywany w §4.3.2. W §4.1.1 odnotowuje się jej dostępność jako cechę strukturalną korpusu, nie konsumpcję w modelach. Decyzja o utrzymaniu trzech odrębnych strumieni zdarzeń — zamiast jednolitego strumienia bazującego wyłącznie na PlayerStats jako agregacie — wynika z faktu, że poszczególne strumienie niosą jakościowo odmienny sygnał: trakerowy umożliwia rekonstrukcję ścieżki ekonomicznej i militarnej z dokładnością do pojedynczego zdarzenia, podczas gdy PlayerStats dostarcza wyłącznie zagregowanych migawek. Oddzielne strumienie tracker / game / message są istotne dla zadania predykcji, ponieważ umożliwiają ekstrakcję cech opartych na sekwencji zdarzeń — formy niedostępnej z dostępu do zagregowanych statystyk meczu (szczegóły w §4.3.2). Trzy odrębne strumienie zdarzeń generują strukturalną przewagę SC2EGSet nad agregowanymi korpusami AoE2 omawianymi w §4.1.2 — przewagę wykorzystywaną w §4.3.2 oraz omawianą jako oś asymetrii eksperymentalnej w §1.4.

#### 4.1.1.3 Schemat analityczny po wstępnym czyszczeniu

W wyniku kroku 01_04 (Pipeline Section 01_04 — Initial Cleaning) powstały trzy widoki DuckDB stanowiące podstawę dalszych faz pracy. Widok `matches_long_raw` jest kanoniczną warstwą *long-skeleton* — jednym wierszem na gracza na mecz — i obejmuje 44 817 wierszy odpowiadających 22 390 powtórkom w relacji dwu-wierszowej na mecz (niezmiennik I5 — symetryczne sloty graczy); dokumentacja schematu znajduje się w `data/db/schemas/views/matches_long_raw.yaml`. Widok `matches_flat_clean` jest celem predykcji — obejmuje 28 kolumn i 44 418 wierszy reprezentujących 22 209 powtórek po zastosowaniu dwóch reguł wykluczenia (szczegóły w Tabeli 4.1). Widok `player_history_all` służy jako źródło historii cech w Phase 02 — obejmuje 37 kolumn i 44 817 wierszy dla wszystkich powtórek, w tym powtórek wykluczonych z celu predykcji, lecz zachowanych jako historia umożliwiająca obliczanie cech czasowo poprzedzających mecz docelowy.

Schemat post-cleaning widoku `matches_flat_clean` obejmuje 28 kolumn w pięciu kategoriach prowenancji zgodnych z niezmiennikiem I3 (dyscyplina temporalna): IDENTITY (identyfikatory meczu i gracza), TARGET (wynik meczu), PRE_GAME (cechy znane przed rozpoczęciem meczu — rasa wybrana, mapa, wersja gry, region), IN_GAME_HISTORICAL (cechy historyczne gracza dla meczów wcześniejszych niż mecz docelowy — dostępne w widoku `player_history_all`, nie w `matches_flat_clean`), oraz CONTEXT (metadane identyfikujące silnik i powtórkę). Pełna specyfikacja dostępna jest w `data/db/schemas/views/matches_flat_clean.yaml`.

Decyzja o utrzymaniu dwóch oddzielnych widoków — `matches_flat_clean` jako celu predykcji oraz `player_history_all` jako źródła historii cech — wynika bezpośrednio z niezmiennika temporalnego I3: cechy wyliczane w Phase 02 muszą operować wyłącznie na stanie danych sprzed rozpoczęcia meczu docelowego, co wymaga jawnego oddzielenia wierszy służących predykcji od wierszy służących agregacji historycznej. Alternatywą byłby pojedynczy widok z flagą `is_target_row` i samodzielnym egzekwowaniem dyscypliny temporalnej w każdej cesze — podejście to odrzucono, ponieważ przenosiłoby odpowiedzialność za zgodność z I3 z warstwy schematu na warstwę kodu cech, zwiększając powierzchnię potencjalnych naruszeń. Szczegóły operacjonalizacji obu widoków w pipeline cech omawia §4.2.3 i §4.3. Utrzymanie 2 wierszy na mecz w widoku `matches_flat_clean` — w przeciwieństwie do 1 wiersza na mecz w `matches_1v1_clean` dla aoestats (omówione w §4.1.2.1) — odzwierciedla strukturalny wybór wynikający ze źródłowego formatu SC2EGSet, w którym każda powtórka dostarcza dwóch zsynchronizowanych perspektyw gracza.

#### 4.1.1.4 Jakość danych: kompletność cech, rankingi i metryki śródmeczowe

Rozkład wyników surowego korpusu — zgodnie z findingiem 01_03_01 — obejmuje 22 382 wiersze Win, 22 409 wierszy Loss, 24 wiersze Undecided oraz 2 wiersze Tie, co po zastosowaniu filtra prawdziwego 1v1 rozstrzygniętego (reguła R01) daje w widoku `matches_flat_clean` idealną symetrię 50,0% Win / 50,0% Loss, potwierdzoną asercją walidacyjną 01_04_02 (18 assertions PASS, wszystkie przeszły). Rozkład rasowy w surowym korpusie wynosi 36,21% Protoss / 35,02% Zerg / 28,76% Terran oraz trzy pojedyncze wiersze z prefiksami Brood War — artefakt szumowy z jednej 6-osobowej powtórki obserwacyjnej odgrywającej SC:BW, klasyfikowany jako szum strukturalny i wykluczany filtrem `true_1v1_decisive` [REVIEW: `01_03_01_systematic_profile.md` raportuje explicite BWTe=1 i BWPr=1 w top-5 race table; trzeci wiersz BWZe inferowany z arytmetyki sumy 16228+15695+12891+1+1=44816 vs total 44817]. Kolumna `selectedRace` zawierała 1 110 wierszy z pustą wartością — odpowiadających 555 powtórkom, w których obaj gracze zadeklarowali losowy wybór rasy; w widokach post-cleaning wartości te zostały znormalizowane do literału `'Random'` zgodnie z regułą cleaning R (reguła wypełniania sentynelu w `01_04_01_data_cleaning.md`).

Kluczowym *findingiem* jakościowym jest niedostępność wskaźnika rankingowego MMR dla dominującej większości korpusu: wartość `MMR=0` pokrywa 83,95% wierszy w `matches_flat_clean` oraz 83,65% wierszy w `player_history_all` zgodnie z ledgerem `01_04_01_missingness_ledger.csv`. Wartość ta jest sentynelowa — w schemacie raportowym Battle.net `MMR=0` oznacza gracza zawodowego niepodpiętego do ladderowego systemu rankingowego (ang. *unrated professional*), nie zaś zerowy poziom umiejętności. Mechanizm tej missingness jest klasyfikowany jako MNAR (missing not at random) wg taksonomii [Rubin1976] — wartość brakuje systematycznie u graczy o określonej charakterystyce (konto profesjonalne bez rejestracji w ladderze), nie losowo. Decyzja DS-SC2-01 (krok 01_04_02) operacjonalizuje tę obserwację przez DROP_COLUMN z zachowaniem flagi binarnej `is_mmr_missing` jako indykatora missingness-as-signal w schemacie scikit-learn MissingIndicator. Wybór DROP_COLUMN z flagą, zamiast imputacji medianą-w-rasie lub retencji z kategorialnym kodowaniem, wynika z trzech argumentów: po pierwsze, zerowej wartości predykcyjnej MMR jako sygnału stałego dla 84% korpusu; po drugie, dostępności pełnej historii cech w `player_history_all` umożliwiającej retrospektywne wyliczenie rankingów Glicko-2 z surowych wyników meczów (omówione w §2.5 i §4.3) niezależnie od pola `MMR` w powtórce; po trzecie, jednorodności decyzji z analogicznymi rozwiązaniami dla korpusów AoE2 (DS-AOESTATS-02 dla aoestats i DS-AOEC-04 dla aoe2companion — omówione w §4.1.2), co zachowuje porównywalność międzykorpusową. Progowa wartość 80% dla rekomendacji DROP_COLUMN dla cechy dominowanej sentynelem pochodzi z reguły S4 operacyjnego przewodnika obsługi missingness, argumentowanej teoretycznie przez [vanBuuren2018] jako granica, powyżej której imputacja staje się strukturalnie nieobronna. Progowa wartość 5% jako granica dla mechanizmu MCAR i rekomendacji RETAIN_AS_IS z prostą imputacją pochodzi z [SchaferGraham2002].

Dostępność wskaźnika APM (akcje na minutę) jest uzupełniająca — parse-kompletna w 97,47% wierszy widoku `player_history_all`, przy 1 132 wierszach (2,53%) z APM=0 jako sentynelem parse-niepowodzenia. Zgodnie z decyzją DS-SC2-10 (01_04_02) zastosowano funkcję `NULLIF(APM, 0)` oraz dodano flagę binarną `is_apm_unparseable` — wzorzec analogiczny do `is_mmr_missing`. Klasyfikacja prowenancji APM jako IN_GAME_HISTORICAL oznacza, że nie może pojawić się w feature-engineeringu jako cecha *pre-game* dla meczu docelowego; jej użycie w cechach historycznych wymaga filtrowania `match_time < T` zgodnie z niezmiennikiem I3 (szczegóły w §4.3). Kontrast dostępności APM (97,47%) z obecnością sentynelu MMR=0 w 83,95% wierszy (por. Tabela 4.4b) jest bezpośrednim świadectwem specyfiki populacji zawodowej: APM jest zawsze parsowalne ze strumienia zdarzeń powtórki, podczas gdy MMR jest wartością zewnętrzną raportowaną przez Battle.net wyłącznie dla graczy ladderowych, a większość meczów turniejowych jest rozgrywana na kontach profesjonalnych nieprzypisanych do ladderowego systemu matchmakingu.

Kolumny `highestLeague` oraz `clanTag` wykazują sentynelowe pokrycia odpowiednio 72,04%/72,16% oraz 73,93%/74,10% (matches_flat_clean / player_history_all); decyzje DS-SC2-02 i DS-SC2-03 orzekają DROP_COLUMN zgodnie z regułą S4 oraz teoretycznym argumentem [vanBuuren2018] przeciwko imputacji cech dominowanych sentynelem — z zachowaniem istniejącej kolumny `isInClan` jako binarnego proxy dla przynależności do klanu. Istnienie tych pól w surowym schemacie odnotowane jest jako udokumentowany koszt parsera `s2protocol` [BlizzardS2Protocol], nie jako usterka korpusu. Kolumna SQ (spending quotient) zawiera sentynel `INT32_MIN` dla 2 wierszy (0,0045%) — parse-artefakt; zastosowano `NULLIF` w `player_history_all` (reguła R05).

Pokrycie parsera na poziomie powtórki jest wysokie: 22 379 z 22 390 powtórek (99,95%) ma dokładnie 2 wiersze graczy, zgodnie z findingiem `01_03_02_true_1v1_profile.md`; pozostałe 11 powtórek ma strukturalnie odmienne liczności (1, 4, 6, 8 lub 9 graczy), odpowiadające powtórkom obserwacyjnym i meczom niestandardowych formatów. Dodatkowo 26 wierszy (13 powtórek) ma wynik Undecided lub Tie — typowo wynik rozłączenia połączenia lub poddania bez deklaracji zwycięzcy — wykluczane filtrem `true_1v1_decisive` zgodnie z zasadą niemodyfikowania wyniku na poziomie targetu. Rozkład długości meczu mierzony w polu `header_elapsedGameLoops` jest dostępny w widoku `player_history_all` (37 kolumn), lecz jego empiryczny rozkład (średnia, mediana, IQR, płoty outlierów) nie jest jeszcze sprofilowany w kroku 01_03 [REVIEW: pełna analiza rozkładu długości meczu zarezerwowana dla Step 01_05 (Temporal & Panel EDA); wartości derywowanego progu wykluczeń długości meczu — zadanie §4.2.3 po 01_05].

#### 4.1.1.5 Asymetrie strony i ograniczenia

W surowym widoku `matches_long_raw` zaobserwowano asymetrię strony planszy: strona 0 wygrywa 51,96% meczów, strona 1 — 47,97% (różnica 3,99 punktu procentowego, poniżej progu alertowego 10 p.p. wyznaczonego operacyjnie w `01_04_00_source_normalization.md`). Decyzja cleaning ogranicza się do udokumentowania asymetrii — korekta na poziomie widoku surowego byłaby nieadekwatna metodologicznie (przepróbkowanie wierszy zmieniłoby liczbę obserwacji i zakłóciłoby ścieżkę CONSORT); randomizacja przypisań *focal* / *opponent* w Phase 02 jest wymogiem niezmiennika I5 i jest przedmiotem §4.3.1.

Wąska reprezentacja populacji jest strukturalną cechą korpusu: `leaderboard_raw` jest NULL dla 100% wierszy `matches_long_raw`, co potwierdza brak meczów z ladderowego systemu matchmakingu i wynika bezpośrednio z projektowego zakresu SC2EGSet jako korpusu turniejowo-zawodowego. Konsekwencje dla generalizacji predykcji — niemożność ekstrapolacji wniosków na populację Battle.net — omówione są w §4.4 i §6.5 jako zagrożenie dla trafności zewnętrznej. Kompletność kolumny mapy obejmuje 188 unikalnych nazw (`01_02_04_univariate_census.md`), przy 273 powtórkach z anomalią `gd_mapSizeX/Y=0` (parse-artefakt); zgodnie z decyzją DS-SC2-06 kolumny mapowania są usunięte z `matches_flat_clean` (redundancja z `metadata_mapName`) i zachowane w `player_history_all` dla przyszłych analiz geometrii mapy. Dryf wersji (*dryf między patchami*) jest istotnym zagrożeniem: 22 390 powtórek obejmuje mecze rozgrywane pod 46 wersjami gry (kardynalność pola `metadata.gameVersion` zgodnie z `01_02_04_univariate_census.md`). Konsekwencje dryfu wersji dla protokołu walidacji omawiane są w §4.4 (split protocol) i §6.5 (threats to validity).

Pełna lista konsekwencji wymienionych ograniczeń dla protokołu eksperymentalnego przedstawiona jest w §4.4; konsekwencje dla trafności wniosków syntetyzuje §6.5. Przepływ danych od surowych plików do widoków post-cleaning — wraz z liczbami wierszy i meczów po każdym filtrze — przedstawia Tabela 4.1. Porównanie skali i asymetrii tego korpusu z korpusami AoE2 omawianymi w §4.1.2 znajduje się w Tabeli 4.4a i Tabeli 4.4b w §4.1.3.

**Tabela 4.1.** CONSORT-style przepływ danych SC2EGSet od surowych plików powtórek do widoków post-cleaning.

| Etap | Mecze (powtórki `.SC2Replay`) | Wiersze gracz×mecz |
|---|---:|---:|
| Surowe pliki `.SC2Replay.json` (acquisition) | 22 390 | n/d |
| `replays_meta_raw` po dekompresji | 22 390 | n/d |
| `replay_players_raw` po dekompresji | n/d | 44 817 |
| `matches_long_raw` (lossless JOIN po `filename`) | 22 390 | 44 817 |
| `matches_flat` (structural JOIN) | 22 390 | 44 817 |
| Po R01 (true_1v1_decisive: -24 mecze) | 22 366 | 44 732 |
| Po R03 (MMR<0 replay-level exclusion: -157 meczów) | 22 209 | 44 418 |
| **`matches_flat_clean` (cel predykcji)** | **22 209** | **44 418** |
| `player_history_all` (źródło historii cech, wszystkie powtórki) | 22 390 | 44 817 |

Źródła liczb: `01_01_01_file_inventory.md` (surowe pliki), `01_04_00_source_normalization.md` (matches_long_raw), `01_04_01_data_cleaning.md` (reguły R01, R03, wiersze końcowe), `01_04_02_post_cleaning_validation.md` (assertions walidacyjne). Reguła R01 = filtr true-1v1-decisive zdefiniowany w `01_04_01_data_cleaning.md` (player_row_count=2, win_count=1, loss_count=1); reguła R03 = wykluczenie replay-level jakiejkolwiek powtórki zawierającej gracza z `MMR<0`. Wiersze gracz×mecz w `matches_flat_clean` to 2× liczba powtórek z założenia dwu-wierszowej struktury per replay (niezmiennik I5).

### 4.1.2 Korpusy Age of Empires II: aoestats i aoe2companion

#### 4.1.2.0 Dlaczego dwa korpusy AoE2

Analiza Age of Empires II w niniejszej pracy opiera się na dwóch komplementarnych korpusach — aoestats [AoEStats] i aoe2companion [AoeCompanion] — z jawnym pominięciem ścieżki parsowania plików zapisu meczu (`.aoe2record`) z biblioteką `aoc-mgz` [MgzParser], zarezerwowanego w §7.3 (Future work). Decyzja o strategii dwukorpusowej — w odróżnieniu od strategii jednokorpusowej stosowanej dla SC2EGSet w §4.1.1 — wynika bezpośrednio z faktu, że żadne z dostępnych źródeł danych AoE2 nie udostępnia surowych plików zapisu meczu na skalę porównywalną z korpusem SC2EGSet [Bialecki2023]. Komplementarność między aoestats (szeroki tygodniowy agregat meczów rankingowych w formacie Parquet, z jedną agregacyjną linią na mecz) a aoe2companion (głębokie dzienne migawki historii każdego gracza, z linią na gracza na mecz) jest substytutem strukturalnej bogactwa replaysowego, niedostępnego w AoE2. Szersze umiejscowienie obu źródeł w ekosystemie danych AoE2 — łącznie z parserem `aoc-mgz` jako ścieżką, której się nie wykorzystuje — znajduje się w §2.3.4.

Strategia dwukorpusowa realizuje trzy cele jednocześnie. Po pierwsze, umożliwia kontrolę próbkowania: wybrane statystyki opisowe można porównać między korpusami, a rozbieżności potraktować jako sygnał idiosynkrazji zbioru, nie zjawiska domenowego. Po drugie, umożliwia rozdzielenie efektu metody od efektu źródła: predykcje trenowane na cechach z aoestats mogą być walidowane na analogicznych cechach z aoe2companion. Po trzecie — i najważniejsze — cechy wymagające długich okien historycznych (kroczący *win rate*, retrospektywne rankingi Glicko-2) korzystają z aoe2companion jako źródła nadrzędnego dzięki głębokiej historii per-gracza, podczas gdy aoestats pełni rolę kontrolnego zbioru o prostszym schemacie (1-row-per-match, omówione w §4.1.2.1). Decyzja o nieposługiwaniu się samym aoestats wynika z agregacyjnej granulacji tego źródła — historie gracza wymagają operacji typu *window function* na wszystkich meczach gracza, nienaturalnych w 1-row-per-match schemacie aoestats. Decyzja o nieposługiwaniu się samym aoe2companion wynika z kosztu obliczeniowego: aoe2companion operuje na 264 mln wierszach player-history, podczas gdy aoestats — na 107 mln; prostszy 1-row-per-match schemat aoestats służy jako punkt odniesienia dla walidacji niektórych cech w prostszej i tańszej formie. Z perspektywy asymetrii eksperymentalnej omówionej w §1.4, obie ścieżki — zawodowa turniejowa (SC2EGSet) i rankingowa ladderowa (dwa korpusy AoE2) — są utrzymywane świadomie jako oś porównania, nie jako nieplanowana asymetria.

#### 4.1.2.1 Korpus aoestats

**Cytowanie i pozyskanie.** Korpus aoestats [AoEStats] jest agregatorem publicznie dostępnym, serwującym tygodniowe zrzuty bazy meczów rankingowych w formacie Parquet, generowane przez crawling API aoe2.net [REVIEW: dokładne źródło crawlera i stabilność mapowania API → Parquet nie są udokumentowane na stronie aoestats.io; charakterystyka oparta jest na obserwowalnym zachowaniu dumpów]. Na podstawie inwentarza plików w kroku 01_01_01 można stwierdzić, że korpus obejmuje 172 tygodniowe pliki Parquet w podkatalogu `matches/` (610,55 MB) oraz 171 tygodniowych plików Parquet w `players/` (3 162,86 MB), uzupełnionych pojedynczym plikiem `overview/overview.json` o metadanych singletonowych — łącznie ~3,77 GB surowego rozmiaru. Różnica jednego pliku między `matches/` a `players/` (172 vs. 171) odpowiada brakowi tygodnia 2025-11-15 → 2025-11-23 w `players/` przy jego obecności w `matches/` [REVIEW: pochodzenie asymetrii w ostatnim tygodniu pobrania niezweryfikowane; możliwe wyjaśnienia to przerwa crawlera lub asynchroniczne wrzucanie plików matches i players; wymaga weryfikacji w następnej iteracji].

Pokrycie czasowe rozciąga się od 2022-08-28 do 2026-02-07 (172 tygodni). W pliku `matches/` występują trzy luki: 2024-07-20 → 2024-09-01 (43 dni), 2024-09-28 → 2024-10-06 (8 dni) oraz 2025-03-22 → 2025-03-30 (8 dni); w pliku `players/` występują cztery luki (te trzy plus dodatkowo 2025-11-15 → 2025-11-23). Luka 43-dniowa w lipcu i sierpniu 2024 koreluje temporalnie z okresem po wprowadzeniu aktualizacji zmieniającej schemat źródłowy API — w tym okresie aoestats.io zatrzymał crawl do czasu zsynchronizowania parsera; w protokole walidacji w §4.4 ten przedział może wymagać dodatkowego okna purge [REVIEW: dokumentacja techniczna przerwy nie jest publicznie dostępna; interpretacja oparta na archiwach społecznościowych].

**Schemat analityczny po wstępnym czyszczeniu.** W wyniku kroku 01_04 powstały trzy widoki DuckDB. Widok `matches_long_raw` (107 626 399 wierszy) jest lossless JOIN `players_raw` × `matches_raw`, przefiltrowany do wierszy z niepustymi `profile_id` oraz `started_timestamp` (wykluczono 1 185 wierszy z `profile_id=NULL`, odpowiadających AI-przeciwnikom w meczach niestandardowych). Widok `matches_1v1_clean` (20 kolumn × 17 814 947 meczów) jest celem predykcji — istotne jest, że aoestats utrzymuje strukturę **1 wiersz na mecz** (nie 2 wiersze jak w SC2EGSet i aoe2companion), w której obaj gracze są zakodowani w kolumnach pivotowanych `p0_*` i `p1_*` (`p0_profile_id`, `p0_civ`, `p0_old_rating`, `p0_winner` oraz symetrycznie `p1_*`). Widok `player_history_all` (14 kolumn × 107 626 399 wierszy) obejmuje wszystkie typy rozgrywki (nie tylko ranked_1v1), służąc jako pełne źródło do obliczania cech historycznych. Decyzja o 1-row-per-match w aoestats nie jest projektowym wyborem pipeline'u — jest cechą formatu źródłowego aoestats (agregacja zdarzeń rankingowych do jednego wiersza per mecz); rzetelne porównanie symetryczności gracz×mecz między korpusami wymaga jawnej konwersji w Phase 02, szczegóły w §4.3.1 i §4.4.1.

**Jakość danych: rozkład Elo, kompletność rankingów, asymetria slotów.** Kompletność cech rankingowych jest w aoestats wysoka. Wartość `p0_old_rating` ma sentynel `=0` w 4 730 wierszach (0,0266% pokrycia), `p1_old_rating` — w 188 wierszach (0,0011%), `avg_elo` — w 118 wierszach (0,0007%); zgodnie z decyzjami DS-AOESTATS-02 i DS-AOESTATS-03 (krok 01_04_02) zastosowano `NULLIF(old_rating, 0)` oraz `NULLIF(avg_elo, 0)` oraz dodano flagi `p0_is_unrated`, `p1_is_unrated` w widoku `matches_1v1_clean` (wzorzec MissingIndicator analogiczny do sc2egset DS-SC2-10). Asymetria między slotami (4 730 vs. 188 sentynelowych wartości) jest sama w sobie diagnostyką — wynika z mechaniki przypisywania gracza do slotu team=0/team=1 w schemacie źródłowym, nie z właściwości graczy. Decyzja o NULLIF z flagą, zamiast retencji 0 jako kategorialnego kodowania *unrated*, wynika z faktu, że 0 w Elo nie jest wartością dopuszczalną w modelach rankingowych opartych na [Elo1978] oraz z potrzeby zachowania semantyki numerycznej dla operacji arytmetycznych na kolumnach ratingu w Phase 02 (np. uśrednianie `avg_elo`). Progowe rekomendacje dla poszczególnych rat missingness (NULLIF dla <1% sentynelu, DROP_COLUMN dla >80%, FLAG_FOR_IMPUTATION dla 5–40%) pochodzą z reguł S3/S4 operacjonalizujących taksonomię [Rubin1976] i [SchaferGraham2002] — stałe 5% i 80% są cytowane wprost w ledgerach missingness (`01_04_01_missingness_ledger.csv`).

Sentynel `team_0_elo = -1` i `team_1_elo = -1` jest nieobecny w zakresie 1v1 ranked (DS-AOESTATS-01 F1 override): filtr upstream `leaderboard = 'random_map'` wyklucza wiersze, w których sentynel ten występował; kolumny pozostają w schemacie jako diagnostyczne dla ewentualnego rozszerzenia zakresu na non-1v1 tryby.

Najważniejszym *findingiem* jakościowym w aoestats jest asymetria stron: w zakresie 1v1 ranked zaobserwowano, że team=1 wygrywa 52,27% meczów (team=0 — 47,73%), zgodnie z `01_04_00_source_normalization.md` („1v1 scoped"). Asymetria 52,27% nie jest losowa — jest funkcją mechaniki przypisywania graczy do slotów team=0/team=1 przez aoestats i zgodnie z diagnostyką `01_02_06_bivariate_eda.md` koreluje z różnicą Elo: średni `elo_diff = team_0_elo − team_1_elo` wynosi -18,48 gdy team=1 wygrywa oraz -0,37 gdy team=0 wygrywa [REVIEW: dokładne wartości `elo_diff` zweryfikowane w T01 z `01_02_06` narrative summary; pełny rozkład elo_diff zarezerwowany dla Step 01_05]. Konsekwencja: każdy model trenowany bez randomizacji *focal*/*opponent* w Phase 02 nauczy się sygnału przypisywania do slotu, nie sygnału umiejętności gry. Niezmiennik I5 wymaga tej randomizacji; szczegóły w §4.3.1.

Reguła R08 wyklucza z widoku `matches_1v1_clean` 997 wierszy (0,0056%) z niespójnymi wynikami (`p0_winner = p1_winner`, 811 oba FALSE, 186 oba TRUE) — traktowane jako artefakt jakości upstream danych aoestats, nie artefakt naszego JOIN. Tak niska skala błędu (~5,6 na 100 000 meczów) uprawnia do uznania źródła za wewnętrznie spójne na poziomie warunków kompletowych.

**Dryf schematu (kolumny *in-game*).** Kolumny wewnątrzgrowe `opening`, `feudal_age_uptime`, `castle_age_uptime`, `imperial_age_uptime` są wypełnione do meczów przed 2024-03-10 (`01_04_01_data_cleaning.md`, „Last week with opening > 1%: 2024-03-10"); od 2024-03-17 pokrycie spada do 0%. Powód: zmiana konfiguracji crawlera aoestats lub zmiana formatu źródłowego API aoe2.net. Dla zachowania spójności pre-game / in-game w niezmienniku I3 kolumny te zostały wykluczone z `matches_1v1_clean` (DS-AOESTATS-04 oraz wcześniejszy I3 cleanup); ewentualne włączenie ich w formie cech historycznych (np. uśredniony *age uptime* jako proxy efektywności otwarcia) jest decyzją Phase 02 (niezmiennik I9).

**Asymetrie i ograniczenia.** aoestats nie dostarcza in-game state — to ograniczenie jest wspólne dla obu korpusów AoE2 i stanowi kluczową oś asymetrii eksperymentalnej między AoE2 a SC2 omawianej w §1.4 i §6.5. Identyfikatory graczy (`profile_id`) są globalnie unikalne w obrębie aoe2.net i przechowywane jako BIGINT (dokładna wartość maksymalna obserwowana w korpusie zarezerwowana do weryfikacji w Pass 2 na podstawie JSON artefaktu `01_04_01_data_cleaning.json`). Pokrycie zakresem 1v1 ranked random_map obejmuje 96,62% prawdziwych meczów 1v1 zgodnie z findingiem `01_03_02_true_1v1_profile.md` (Jaccard index między zbiorem „true 1v1" a „ranked 1v1" wynosi 0,958755); pozostałe 3,38% to mecze co_random_map (1v1 na mapach kooperacyjnych, 622 817 meczów) i śladowe wejścia team_random_map / co_team_random_map. Decyzja o zawężeniu zakresu celu predykcji do `leaderboard = 'random_map'` (reguła R02) wynika z chęci homogenizacji trybu gry — mecze co_random_map mają odmienne zasady inicjalizacji mapy i asymetryczny dostęp do zasobów, czyniąc je nieporównywalnymi statystycznie z ranked 1v1.

**Tabela 4.2.** CONSORT-style przepływ danych aoestats.

| Etap | Mecze | Wiersze gracz×mecz |
|---|---:|---:|
| Surowe pliki Parquet (acquisition) | n/d | n/d |
| `matches_raw` po ingestion | 30 690 651 | n/d |
| `players_raw` po ingestion | n/d | 107 627 584 |
| Po ingestion-level filter (profile_id, started_timestamp IS NOT NULL) | n/d | 107 626 399 |
| `matches_long_raw` (lossless JOIN) | n/d | 107 626 399 |
| Po 1v1 structural filter (COUNT(*)=2 AND COUNT(DISTINCT team)=2 per match) | 18 438 769 | 36 877 538 |
| Po `leaderboard='random_map'` filter | 17 815 944 | 35 631 888 |
| Po R08 inconsistent-winner exclusion (−997 meczów) | 17 814 947 | 35 629 894 |
| **`matches_1v1_clean` (cel predykcji, 1-row-per-match)** | **17 814 947** | **17 814 947** |
| `player_history_all` (źródło historii, wszystkie leaderboardy) | n/d | 107 626 399 |

Źródła liczb: `01_01_01_file_inventory.md`, `01_04_00_source_normalization.md`, `01_04_01_data_cleaning.md` (CONSORT Flow), `01_03_02_true_1v1_profile.md`. Wiersze gracz×mecz w `matches_1v1_clean` są równe liczbie meczów z powodu 1-row-per-match struktury aoestats (kolumny `p0_*` / `p1_*` zawierają oba gracze w jednym wierszu); wartość 35 629 894 = 2 × 17 814 947 podano dla porównywalności z `player_history_all`.

#### 4.1.2.2 Korpus aoe2companion

**Cytowanie i pozyskanie.** Korpus aoe2companion [AoeCompanion] jest projektem mobilnej aplikacji towarzyszącej z dedykowanym REST API udostępniającym pełne historie meczowe per-gracza — w odróżnieniu od aoestats, który agreguje po meczach, aoe2companion udostępnia rekordy per-gracza per-mecz z kompletnymi metadanymi sesji. Na podstawie inwentarza plików w kroku 01_01_01 można stwierdzić, że korpus obejmuje 2 073 dzienne pliki Parquet w podkatalogu `matches/` (6 621,52 MB), 2 072 dzienne pliki CSV w `ratings/` (2 519,59 MB), oraz dwa pojedyncze snapshoty: `leaderboards/leaderboard.parquet` (83,32 MB) i `profiles/profile.parquet` (161,84 MB) — łącznie ~9,39 GB surowego rozmiaru.

Pokrycie czasowe: matches 2020-08-01 — 2026-04-04 (2 073 dni, bez luk); ratings 2020-08-01 — 2026-04-04 (jedna mała luka 2025-07-10 → 2025-07-12, 2 dni). Codzienne migawki dziennej granulacji w aoe2companion stoją w kontraście z tygodniowymi migawkami w aoestats — oznacza to głębsze pokrycie temporalne kosztem zwiększonej redundancji (ten sam mecz może być zapisany w wielu dziennych snapshotach); szczegóły deduplikacji znajdują się w regułach cleaning R02 omawianych poniżej oraz w §4.2.

**Schemat analityczny.** Widok `matches_long_raw` jest lossless projekcją z `matches_raw` (277 099 059 wierszy = identyczny jak w źródle), z 74 788 989 odrębnymi identyfikatorami meczu (`matchId`); liczba meczów jest zatem prawie czterokrotnie większa niż w aoestats, przy prawie trzykrotnie większej liczbie wierszy player-row. Widok `matches_1v1_clean` (48 kolumn × 61 062 392 wierszy = 30 531 196 meczów) jest celem predykcji; istotne jest, że aoe2companion utrzymuje strukturę **2 wierszy na mecz** (player-row-oriented) — w przeciwieństwie do aoestats 1-row-per-match. Decyzja o player-row-oriented schemacie w `matches_1v1_clean` aoe2companion wynika bezpośrednio z formatu źródłowego REST API per-gracza — zachowano natywną granulację danych zamiast agregować po meczach; zaletą jest brak konieczności rozplatania kolumn `p0_*`/`p1_*` dla cech indywidualnych, wadą — podwojona objętość przechowywania i konieczność JOIN po `matchId` przy obliczaniu cech meczu (w aoestats cechy meczu są naturalnym `SELECT` na jednym wierszu, w aoe2companion — wymagają JOIN na identyfikatorze meczu). Widok `player_history_all` (19 kolumn × 264 132 745 wierszy) obejmuje wszystkie typy rozgrywki dla pełnego zakresu obliczania cech historycznych (wszystkie leaderboardy, nie tylko ranked_1v1).

**Jakość danych.** Najważniejszym *findingiem* w aoe2companion jest kompletność cechy `rating` (Elo wchodzące do meczu): w `matches_1v1_clean` kolumna ta ma 15 999 234 wierszy z NULL (26,20%), co oznacza V1 rating coverage 73,80% (`01_04_01_data_cleaning.md`). Zgodnie z decyzją DS-AOEC-04 zastosowano RETAIN + flaga binarna `rating_was_null` (wzorzec sklearn MissingIndicator). Wysoki rate missingness (26,20%) jest cechą populacji aoe2companion — obejmuje wszystkie ranked 1v1 leaderboardy (`internalLeaderboardId IN (6, 18)`), w tym mecze sezonowe, w których gracze nie mieli jeszcze przypisanej wartości `rating` lub wartość była niezarejestrowana w momencie crawlingu. Decyzja FLAG_FOR_IMPUTATION zamiast DROP_COLUMN wynika z wyjątku reguły S4 dla cech primary-first-order (wyjątek [vanBuuren2018] dla cech, których wartość informacyjna przeważa nad kosztem missingness): rating jest cechą predykcyjną pierwszego rzędu — jego usunięcie oznaczałoby utratę ~74% zachowanego sygnału na rzecz uniknięcia 26% missingness.

Cecha `country` ma w `matches_1v1_clean` NULL w 2,25% wierszy oraz w `player_history_all` — 8,30% (przekracza granicę <5% MCAR z [SchaferGraham2002]); decyzja per-VIEW odroczona do Phase 02 (Rule S2 — target null rows), z rekomendacją FLAG_FOR_IMPUTATION w historii z uwagi na przekroczenie granicy MCAR.

Kolumny ustawień rozgrywki wykazują szeroką paletę mechanizmów missingness, dokumentowaną w ledgerze `01_04_01_missingness_ledger.csv`. Kolumna `server` ma 97,39% NULL (MNAR — DROP per reguła S4 / [vanBuuren2018]); `scenario` i `modDataset` — 100% NULL (DROP, brak informacji po filtrowaniu ranked 1v1); `password` — 77,57% NULL (DROP ścieżką 40–80% MAR-non-primary); `antiquityMode` — 60,06% NULL (DROP przez interpretację schematowo-ewolucyjną — wprowadzona w późniejszym patchu, missingness zależy od patchu meczu); `hideCivs` — 37,18% NULL (FLAG_FOR_IMPUTATION, 5–40% band). Cała paleta rekomendacji jest zbudowana wokół operacyjnych progów 5% (MCAR, [SchaferGraham2002]), 40% i 80% (reguła S4, argument [vanBuuren2018]) — cytowanych wprost w kolumnie `recommendation_justification` ledgera.

Zgodnie z regułą R04 kroku 01_04_01, dziesięć kolumn ustawień gry (`allowCheats`, `lockSpeed`, `lockTeams`, `recordGame`, `sharedExploration`, `teamPositions`, `teamTogether`, `turboMode`, `fullTechTree`, `population`) ma wartości NULL jednocześnie w 11 184 wierszach (<0,02% korpusu); flaga `is_null_cluster=TRUE` utrzymana w schemacie jako indykator, nie jako podstawa wykluczenia. Cluster obejmuje cały zakres dat korpusu i ma charakter informacyjny.

Kolumna `won` (target predykcji) ma 0 NULL w `matches_1v1_clean` dzięki regule R03 (każdy mecz ma dokładnie jedną wartość TRUE i jedną FALSE); w `player_history_all` występuje 19 251 NULL (0,0073%) — mecze z leaderboardów niewłączonych do zakresu ranked_1v1. Decyzja DS-AOEC-07 zakłada EXCLUDE_TARGET_NULL_ROWS z fizycznym wykluczeniem odroczonym do Phase 02 (reguła S2: nigdy nie imputować targetu). Identyfikatory profileId=-1 (gracze AI plus parse-failed-player) zostały wykluczone upstream (reguła R00 + R02) — w wyniku 12 947 078 wierszy AI (4 150 733 meczów z AI) oraz 19 232 wierszy parse-failed (8 993 meczów) usunięto ze scope'u, zgodnie z findingiem `01_03_02_true_1v1_profile.md`. To samo zjawisko występuje w aoestats — tam AI-partycypanci mają NULL `profile_id` i są filtrowani naturalnie.

**Artefakt kodowania stron.** aoe2companion używa schematu `team=1` i `team=2` jako stron 1v1 w polu `team`, nie `team=0` i `team=1` jak sugeruje kanonicznie long-skeleton. W mapowaniu `team IN (0, 1) → side`, strona 0 zawiera 449 wierszy, strona 1 — 130 369 073 wierszy (`01_04_00_source_normalization.md`, symmetry audit). Konwersja team→side na poziomie `matches_long_raw` używa wyrażenia `CASE WHEN` traktującego team=1 i team=2 jako dwie strony; szczegóły DDL znajdują się w schemacie YAML widoku. W 1v1 scope (`internalLeaderboardId IN (6, 18)`) asymetria `team1_wins` wynosi 47,1793% — strona team=1 wygrywa mniej meczów niż strona team=2 (52,82%), zgodnie z asercją 1v1-scoped w `01_04_00_source_normalization.md` (linia 54). Konsekwencja jest analogiczna do aoestats i SC2EGSet: niezmiennik I5 wymaga randomizacji *focal*/*opponent* w Phase 02; szczegóły w §4.3.1.

**Asymetrie i ograniczenia.** Jak w aoestats, aoe2companion nie udostępnia in-game state (już odnotowane jako wspólna cecha AoE2 w §4.1.2.0). Skala surowego korpusu (264 132 745 wierszy `player_history_all` vs. 107 626 399 dla aoestats) oznacza wyższe wymagania pamięciowe — wszystkie zapytania są wykonywane za pośrednictwem DuckDB z trybem *spill-to-disk*. Redundancja dzienna (ten sam mecz w wielu snapshotach) wymaga deduplikacji po parze `(matchId, profileId)` z `ORDER BY started` (reguła R02) — impact to wykluczenie 5 wierszy duplikatowych plus 1 wiersz `profileId=-1`, co jest skalą zaniedbywalną w korpusie 264M wierszy, lecz wymagająca jawnej reguły w schemacie.

**Tabela 4.3.** CONSORT-style przepływ danych aoe2companion.

| Etap | Mecze | Wiersze gracz×mecz |
|---|---:|---:|
| Surowe pliki Parquet (acquisition) | n/d | n/d |
| `matches_raw` po ingestion | 74 788 989 | 277 099 059 |
| Po R00 `status='player'` filter (−12 947 078 ai rows, −4 150 733 meczów z AI) | 70 638 256 | 264 151 981 |
| Po R02 `profileId != -1` filter (−19 232 parse-failed-player rows, −8 993 meczów) | 70 629 263 | 264 132 745 |
| `matches_long_raw` (kanoniczna projekcja) | 70 629 263 | 264 132 745 |
| Po R01 `internalLeaderboardId IN (6, 18)` (rm_1v1 + qp_rm_1v1) filter | 30 536 248 | 61 071 799 |
| Po R02 deduplikacji (matchId, profileId) ORDER BY started (−5 duplikatów, −1 profileId=-1) | 30 536 248 | 61 071 794 |
| Po R03 1v1 complementarity HAVING COUNT(*)=2 z TRUE+FALSE won (−5 052 meczów) | 30 531 196 | 61 062 392 |
| **`matches_1v1_clean` (cel predykcji, 2 wiersze na mecz)** | **30 531 196** | **61 062 392** |
| `player_history_all` (źródło historii, wszystkie leaderboardy) | n/d | 264 132 745 |

Źródła liczb: `01_01_01_file_inventory.md`, `01_03_02_true_1v1_profile.md`, `01_04_00_source_normalization.md`, `01_04_01_data_cleaning.md` (CONSORT Flow). Uwaga strukturalna: aoe2companion utrzymuje player-row-oriented schemat (2 wiersze na mecz w `matches_1v1_clean`) — w przeciwieństwie do aoestats (1-row-per-match z kolumnami `p0_*` / `p1_*`).

#### 4.1.2 Podsumowanie i forward-reference do §4.1.3

Przedstawione w §4.1.2.1 i §4.1.2.2 charakterystyki dwóch korpusów AoE2 pokazują dwa wymiary asymetrii istotne dla protokołu eksperymentalnego: wewnątrzkorpusową (1-row vs. 2-row schemat, trzy- vs. jednokolumnowy schemat ratingu, sentynelowy vs. NULL mechanizm missingness), a także wspólne dla obu korpusów ograniczenie strukturalne (brak in-game state niedostępnego w surowych danych AoE2). Pełna macierz asymetrii informacyjnej między korpusem SC2EGSet a oboma korpusami AoE2 — wraz z tablicami 4.4a (Skala i akwizycja) oraz 4.4b (Asymetria analityczna) — przedstawiona jest w §4.1.3. §4.3 operacjonalizuje te asymetrie w schemacie wspólnych cech pre-game (§4.3.1) oraz dokłada do nich specyficzne dla SC2 cechy in-game (§4.3.2); §4.4 operuje na nich w protokole temporalnego splitu.

### 4.1.3 Asymetria korpusów — ramy porównawcze

Dwie tabele przedstawione w tym podrozdziale — Tabela 4.4a dla skali i warunków akwizycji, Tabela 4.4b dla właściwości analitycznych post-cleaning — są rozdzielone świadomie: skala i pokrycie czasowe korpusu są współrzędnymi decyzji o próbkowaniu i walidacji temporalnej (§4.4), podczas gdy właściwości analityczne dotyczą operacjonalizacji schematu cech i targetu (§4.3 oraz §4.4). Rozdzielenie pozwala na niezależną aktualizację każdej z warstw wraz z kolejnymi krokami Phase 01 (w szczególności 01_05 Temporal & Panel EDA oraz 01_06 Decision Gates) bez potrzeby rewizji całej macierzy asymetrii. Pełne uzasadnienie dwukorpusowej strategii dla AoE2 znajduje się w §4.1.2.0; pełne charakterystyki poszczególnych korpusów — w §4.1.1 i §4.1.2.

**Tabela 4.4a.** Skala i akwizycja trzech korpusów.

| Wymiar | SC2EGSet | aoestats | aoe2companion |
|---|---|---|---|
| Gra | StarCraft II | Age of Empires II DE | Age of Empires II DE |
| Źródło | Pliki `.SC2Replay` [Bialecki2023] | API agregator aoestats.io [AoEStats] | REST API aoe2companion [AoeCompanion] |
| Surowy rozmiar | ~214 GB | ~3,77 GB | ~9,39 GB |
| Liczba plików (acquisition) | 22 390 plików `.SC2Replay.json` | 172 + 171 Parquet (matches/players) + 1 overview | 2 073 + 2 072 (matches/ratings) + 2 snapshoty |
| Pokrycie czasowe | 2016-01-07 — 2024-12-01 (turniejowe, nieciągłe, 32 luki miesięczne) | 2022-08-28 — 2026-02-07 (3 luki w matches, 4 w players) | 2020-08-01 — 2026-04-04 (brak luk w matches, 1 w ratings) |
| Granulacja archiwum | 70 katalogów turniejowych | tygodniowa | dzienna |
| Populacja | Zawodowa turniejowa | Ladder rankingowy 1v1 random_map | Ladder rankingowy 1v1 (rm_1v1 + qp_rm_1v1) |

Źródła: `01_01_01_file_inventory.md` w katalogach `reports/artifacts/01_exploration/01_acquisition/` odpowiednich korpusów; dla SC2EGSet dodatkowo `01_02_04_univariate_census.md` (zakres `details.timeUTC`) i `01_03_01_systematic_profile.md` (liczba luk miesięcznych).

Argumentacja porównawcza: strukturalna różnica między SC2EGSet (pliki zapisu z pełnymi strumieniami zdarzeń) a korpusami AoE2 (agregowane statystyki meczu + historia rankingowa) wyznacza zakres cech, które są w ogóle dostępne do modelowania. W SC2 można zbudować cechy typu *build order*, kontrolowania mapy, momentów reakcji; w AoE2 — wyłącznie cechy pre-game oraz agregaty historyczne (kroczący *win rate*, retrospektywne rankingi, tempo nabywania rankingu). Konsekwencja dla strategii wspólnej: pre-game feature set (§4.3.1) jest wykonalny w obu grach; SC2-specific in-game features (§4.3.2) pozostają samodzielną osią eksperymentu (asymetria celowa per §1.4). Asymetria wewnątrz AoE2 — 1-row vs. 2-row schemat `*_clean`, trzy- vs. jednokolumnowy schemat ratingu (aoestats: `p0_old_rating` + `p1_old_rating` + `avg_elo`; aoe2companion: `rating` per wiersz) — wyjaśnia różnicę kosztu w implementacji: aoestats wymaga konwersji do 2-wierszowej per-player orientacji w Phase 02 dla operacji symetrycznych, aoe2companion dostarcza tę orientację natywnie, lecz kosztem większej liczby wierszy.

**Tabela 4.4b.** Asymetria analityczna trzech korpusów po wstępnym czyszczeniu (Phase 01 / Pipeline Section 01_04).

| Wymiar | SC2EGSet | aoestats | aoe2companion |
|---|---|---|---|
| Liczba meczów (post-cleaning) | 22 209 (true 1v1 decisive) | 17 814 947 (1v1 random_map) | 30 531 196 (1v1 ranked: rm_1v1 + qp_rm_1v1) |
| Wiersze per mecz w `*_clean` | 2 (player-row) | 1 (kolumny `p0_*`/`p1_*`) | 2 (player-row) |
| Liczba kolumn `matches_*_clean` | 28 | 20 | 48 |
| Liczba kolumn `player_history_all` | 37 | 14 | 19 |
| Wiersze `player_history_all` | 44 817 | 107 626 399 | 264 132 745 |
| Strumienie zdarzeń in-game | 3 (tracker 62 003 411 / game 608 618 823 / message 52 167) | brak | brak |
| Cechy in-game w `*_clean` | brak (I3 wyłączone do Phase 02) | brak (I3 wyłączone) | brak (I3 wyłączone) |
| Asymetria stron (winning slot pct, 1v1 scope) | side=0: 51,96% | team=1: 52,27% | team=2: 52,82% (team=1: 47,18%) |
| Kolumna(-y) ratingu | MMR (DROPPED, 83,95% sentynel) → flaga `is_mmr_missing` | `p0_old_rating` + `p1_old_rating` + `avg_elo` | `rating` (1 kolumna) + flaga `rating_was_null` |
| Sentynel ratingu (odsetek wierszy) | MMR=0: 83,95% | avg_elo=0: 0,0007% | rating NULL: ~26,20% |
| Mechanizm dominującej missingness | MNAR (MMR=0 unrated prof.) | MCAR (low rates: 0,0266% p0, 0,0011% p1) | MAR (26,20% — schema-evolution / patch boundary) |
| Schema-evolution kolumny wykluczone | gd_mapSizeX/Y=0 (273 wierszy) | opening + 3× age_uptime (cut-off 2024-03-10) | 10-kolumnowy NULL-cluster (11 184 wierszy), antiquityMode 60,06%, server 97,39% |
| Kanoniczny identyfikator gracza | `toon_id` (Battle.net, kardynalność 2 495) | `profile_id` (BIGINT) | `profileId` (INTEGER) |

Źródła: `01_04_01_data_cleaning.md`, `01_04_01_missingness_ledger.csv`, `01_04_02_post_cleaning_validation.md` oraz schematy YAML widoków (`data/db/schemas/views/*.yaml`) dla każdego z trzech korpusów. Konwencja liczb: wartości procentowe zaokrąglone do setnych, liczby z ledgerów missingness cytowane w notacji Polish-typography (spacja jako separator tysięcy).

Tabela 4.4b ujawnia trzy osie eksperymentalnej asymetrii, do których §4.3 i §4.4 muszą się odnieść. Po pierwsze, dostępność in-game state jest zero-one: SC2EGSet dostarcza ją, oba korpusy AoE2 — nie; pre-game feature set jest zatem jedynym wspólnym mianownikiem porównania krzyżowego (§4.3.1, §4.4.4), a in-game features pozostają kontrolnym wymiarem eksperymentu dla SC2 (§4.3.2). Po drugie, mechanizmy dominującej missingness są strukturalnie różne: MNAR w SC2 (sentynel niespecyfikowany przez Battle.net dla turniejowych unrated), MCAR w aoestats (bardzo niski rate sentynelu), MAR w aoe2companion (26% NULL skorelowane z patchem i leaderboardem) — co oznacza, że strategia imputacji musi być per-korpus uzasadniona, nie globalnie ujednolicona (zgodnie z argumentem [vanBuuren2018]). Po trzecie, asymetria stron — obecna w SC2EGSet (51,96 pp. / 47,97 pp.) i w aoestats (52,27 pp. / 47,73 pp.) — wymaga randomizacji *focal*/*opponent* w Phase 02 jako warunku spełnienia niezmiennika I5 (§4.3.1, §4.4.1); w aoe2companion, ze struktury 2-wierszowej, asymetria ta nie jest obserwowalna na poziomie widoku bez dalszego przetwarzania, lecz wymóg randomizacji obowiązuje nadal ze względu na potencjalną asymetrię w kodowaniu `team=1` vs. `team=2` w źródłowym API.

Konsekwencje operacyjne powyższej macierzy dla dalszych podrozdziałów: §4.2 opisuje reguły cleaning i walidacji formalizujące decyzje DS-* odnotowane w §4.1.1–§4.1.2; §4.3.1 wprowadza wspólny pre-game feature set (punkt odniesienia obu gier) oraz szczegółowe definicje cech; §4.3.2 wprowadza specyficzne dla SC2 cechy in-game korzystające ze strumieni zdarzeń; §4.3.3 wprowadza specyficzne dla AoE2 cechy z udziałem kategorycznej cywilizacji; §4.4.1 definiuje per-player temporal split operacjonalizujący asymetrie temporalne udokumentowane w Tabeli 4.4a; §4.4.4 definiuje protokół ewaluacji pozwalający wyciągać wnioski przy udokumentowanej asymetrii informacyjnej. Konsekwencje dla trafności wniosków — w szczególności ograniczenia ekstrapolacji z populacji zawodowej (SC2EGSet) na populację ladderową (AoE2) i odwrotnie — są przedmiotem §6.5.

## 4.2 Data preprocessing

### 4.2.1 Ingestion and validation

<!--
Two-path pipeline, canonical replay_id, join validation.
DRAFTABLE — Phase 01 (Data Exploration), Pipeline Section 01_01 complete.
-->

### 4.2.2 Player identity resolution

<!--
Toon fragmentation, nickname as canonical ID, multi-toon classification.
Player coverage stats, cold-start players.
BLOCKED — Phase 01 (Data Exploration), Pipeline Sections 01_02–01_03.
-->

### 4.2.3 Cleaning rules and valid corpus

<!--
Each exclusion rule with empirical motivation. Duration threshold derivation.
Cleaning impact quantification.
BLOCKED — Phase 01 (Data Exploration), Pipeline Section 01_04.
-->

## 4.3 Feature engineering

### 4.3.1 Common pre-game feature set (both games)

<!--
Elo/Glicko-2, rolling win rate, activity, H2H, tournament momentum, career stats.
Symmetric formulation: focal_player + opponent + context.
BLOCKED — Phase 02 (Feature Engineering).
-->

### 4.3.2 SC2-specific in-game features

<!--
PlayerStats fields at canonical timepoints, separability analysis.
BLOCKED — Phase 01 (Data Exploration), Pipeline Section 01_05; Phase 02 (Feature Engineering).
-->

### 4.3.3 AoE2-specific features

<!--
Civilisation pick, map type, Elo-derived.
BLOCKED — AoE2 roadmap.
-->

## 4.4 Experimental protocol

### 4.4.1 Train/validation/test split strategy

<!--
Per-player temporal split. Why per-game splits cause leakage.
Comparison with naïve global split.
BLOCKED — Phase 03 (Splitting & Baselines).
-->

### 4.4.2 Model configurations

<!--
LR, RF, LightGBM/XGBoost, Elo/Glicko baseline. Neural nets if used.
BLOCKED — Phase 03 (Splitting & Baselines); Phase 04 (Model Training).
-->

### 4.4.3 Hyperparameter tuning protocol

<!--
Validation-set-based, no test set peeking.
BLOCKED — Phase 04 (Model Training).
-->

### 4.4.4 Evaluation metrics

<!--
Primary: Brier score (Murphy decomposition), log-loss.
Discrimination: accuracy, ROC-AUC, calibration curves (ECE).
Stratified: per-matchup, cold-start strata, sharpness histograms.
Within-game: Friedman omnibus + Wilcoxon/Holm + Bayesian signed-rank on CV folds.
Cross-game (N=2 games): per-game rankings with bootstrapped CIs, 5x2 cv F-test,
qualitative concordance. Friedman inapplicable with N=2 (Demsar 2006).
See THESIS_WRITING_MANUAL.md §3.2.
SKELETON — can draft from literature.
-->
