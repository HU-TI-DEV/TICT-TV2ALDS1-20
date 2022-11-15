# Uitleg van de bestanden

In deze folder staan een aantal bestanden voor de eindopracht Gomoku van ALDS, hieronder een uitleg van de bestanden.

### Programmas
Er zijn twee programma's in deze map `competition.py` en `gomoku_easy_test_environment.py`. De eerste kan je gebruiken om een comptetitie op te zetten tussen verschillende AI's en de tweede kan je gebruiken om jouw AI door een test suite te testen.


### AI's
De volgende bestanden zijn AI spelers waartegen je kan testen/spelen, je kan ze includen om tegen te testen in de competition / test environment
```
gomoku_ai_marius1_webclient.py
gomoku_ai_random_webclient.py
random_agent.py
```

### Libraries
De volgende bestanden bevatten code voor de competition en test environment.

```
basePlayer.py           -- Base class voor een gomoku speler
gomoku.py               -- Logica voor het uitvoeren van een potje gomoku
GmGame.py               -- Logica voor het visueel weergeven van een gomoku spel
GmGameRules.py          -- Game logica en spelregels voor gomoku
GmQuickTests.py         -- Tests die gebruikt worden om jouw AI te testen
GmUtils.py              -- Utility functies voor AI's.py
```

### Utilities
`gomoku_ai_random_webserver.py` bevat code voor het draaien van een gomoku webserver! Handig als je als docent je AI code niet wilt prijsgeven maar wel wilt meedoen in een competitie 😎

