from flask import Flask

from simulation import run_simulations

app = Flask(__name__)

@app.route('/')
def trigger_simulation():
    run_simulations()
    return 'Finished running simulations!'
