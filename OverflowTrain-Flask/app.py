from flask import Flask, render_template

# from OverflowTrain_CV.destination_providerv2 import CVDestinationProvider
from destination_providerv2 import CVDestinationProvider

app = Flask(__name__)

provider = CVDestinationProvider(7)

@app.route('/')
def index():
    return provider.getNextDestination(["1", "2", "3"])