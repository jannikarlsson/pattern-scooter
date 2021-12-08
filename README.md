[![CircleCI](https://circleci.com/gh/jannikarlsson/pattern-scooter/tree/main.svg?style=svg)](https://circleci.com/gh/jannikarlsson/pattern-scooter/tree/main)

# Cykelklienten

## Simulering

Använd `python3 simulation.py` för att köra en simulering. Antal scootrar som hämtas och maximal simuleringstid kan ändras i `simulation.py`.

## Interaktiv körning

Använd `python3 interactive.py` utan argument för att få möjlighet att köra klienten interaktivt i terminalen. Du kommer att få ange scooterns id och användarens id först, sedan kommer en enkel meny upp där du kan göra olika val.

```
start: startar uthyrningen
move: flyttar scootern ett steg mot målet
stop: avslutar uthyrningen
see: printar info om scootern
charge: laddar till 100 procent
return: avslutar programmet
```