# Cykelklienten

## Interaktiv körning

Använd `python3 app.py` utan argument för att få möjlighet att köra klienten interaktivt i terminalen. Du kommer att få skicka in scooterns id (välj 1-4) och användarens id (valfri siffra, ingen databaskoppling just nu) först, sedan kommer en enkel meny upp där du kan göra olika val.

```
see: printar info om scootern
start: startar scootern och skriver användaren till databasen
stop: stannar scootern och skriver ny info till databasen
faster: ökar hastigheten 1 kph
slower: minskar hastigheten 1 kph
move: kommer att fråga efter lat och lon och flytta scootern (men skriver i nuläget inte till databas om du inte kör en simulering)
charge: laddar till 100 procent (men skriver i nuläget inte till databas om du inte kör en simulering)
run: snabbsimulerar en kort resa
return: avslutar programmet
```
## Snabbsimulering

För att köra en snabbsimulering direkt skickar du in argument när du startar programmet: `python3 app.py --id <scooterid just nu 1-4> --user <userid> --runtime <körtid i sekunder> --delay <väntetid i sekunder innan resan startar>`

Exempel: ```python3 app.py --id 1 --user 34 --runtime 20 --delay 5```

I snabbsimuleringen slumpas hastighet och ny position varje sekund och batterinivån sjunker en procent.

## Databasen
Klienten är nu kopplad till backend (localhost:8080).