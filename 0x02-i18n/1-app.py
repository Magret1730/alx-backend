#!/usr/bin/env python3
""" Flask App Initialization file """
from flask import Flask, render_template
from flask_babel import Babel

# Initialize app from flask
app = Flask(__name__)


class Config:
    """ Config class for the langauges """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


# Use Config to configure the app
app.config.from_object(Config)

# Initialize Babel
babel = Babel(app)


@app.route('/')
def home():
    """ A simple / route """
    return render_template('0-index.html')


if __name__ == '__main__':
    """ Main Function """
    app.run(debug=True)
