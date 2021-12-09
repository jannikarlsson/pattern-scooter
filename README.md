[![CircleCI](https://circleci.com/gh/jannikarlsson/pattern-scooter/tree/main.svg?style=svg)](https://circleci.com/gh/jannikarlsson/pattern-scooter/tree/main) [![codecov](https://codecov.io/gh/jannikarlsson/pattern-scooter/branch/main/graph/badge.svg?token=M7OUB0KUIE)](https://codecov.io/gh/jannikarlsson/pattern-scooter) [![Maintainability](https://api.codeclimate.com/v1/badges/d520f7cce27da41d4490/maintainability)](https://codeclimate.com/github/jannikarlsson/pattern-scooter/maintainability)

# Scooter client
This repository is part of a group project done for the ['pattern' course](https://www.bth.se/utbildning/program-och-kurser/kurser/20232/BR4QJ/) at Blekinge Institute of Technology. Note that the application is part of a larger system. The main repository can be found here: [pattern-orchestra](https://github.com/datalowe/pattern-orchestra)

To clone the repository, run `git clone https://github.com/jannikarlsson/pattern-scooter.git`

To install dependencies, run `pip install -r requirements.txt`

## Simulation mode

Use `python3 simulation.py` to start a simulation of scooters from the database. The default number of scooters is 800, which can be changed in `.env`, along with the default 30 second length of a journey. The scooters are run in separate threads, the number of which can also be changed in `.env`, to offset the trips and enable concurrent requests to the backend service. The simulation will stop when all scooters have run.

## Interactive mode

Use `python3 interactive.py` to run the client interactively in the terminal. You will be prompted for the scooter id and user id, and then get a menu with various options.

```
start: starts rental and turns engine on
move: moves the scooter toward the target position and lowers the battery
stop: turns the engine off and ends rental
see: prints all info about the scooter
charge: charges the scooter battery to 100 %
return: leaves the interactive mode
```
