from flask import Flask, render_template
from model import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cn')
def cn():
    pass


@app.route('/en')
def en():
    pass


