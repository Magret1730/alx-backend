#!/usr/bin/env python3
""" Flask App Initialization file """
from flask import Flask, render_template, g, request
from flask_babel import Babel, _

# Initialize app from flask
# Versions used flask==2.0.3 werkzeug==2.0.3 flask_babel==3.0.0
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


@babel.localeselector
def get_locale():
    """
    if a user is logged in, use the locale from the user settings;
    otherwise try to guess the language from the user accept
    header the browser transmits
    """
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    # Use best_match to determine the best match for the supported languages
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def home():
    """ A simple / route """
    return render_template('3-index.html')


if __name__ == '__main__':
    """ Main Function """
    app.run(debug=True)
