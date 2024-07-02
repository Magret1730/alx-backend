#!/usr/bin/env python3
""" Flask App Initialization file """
from flask import Flask, render_template


# Initialize app from flask
app = Flask(__name__)


@app.route('/')
def home():
    """ A simple / route """
    render_template('templates/0-index.html')


if __name__ == '__main__':
    """ Main Function """
    app.run(debug=True)
