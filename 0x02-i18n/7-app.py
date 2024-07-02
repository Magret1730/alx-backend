#!/usr/bin/env python3
""" Flask App Initialization file """
from flask import Flask, render_template, request, g
from flask_babel import Babel, _

import pytz
from pytz.exceptions import UnknownTimeZoneError

# Initialize app from flask
app = Flask(__name__)


class Config:
    """ Config class for the languages and time zones """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


# Use Config to configure the app
app.config.from_object(Config)


# Initialize Babel
babel = Babel(app)


# Mock user table
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """Returns a user dictionary or None if the ID cannot be
    found or if login_as was not passed."""
    try:
        user_id = int(request.args.get('login_as'))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """Set g.user before each request"""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """
    Determine the best match with our supported languages.
    """
    # 1. Locale from URL parameters
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    # 2. Locale from user settings
    user = g.get('user', None)
    if user and user['locale'] in app.config['LANGUAGES']:
        return user['locale']

    # 3. Locale from request header
    return request.accept_languages.best_match(app.config['LANGUAGES'])

    # 4. Default locale
    return app.config['BABEL_DEFAULT_LOCALE']


@babel.timezoneselector
def get_timezone():
    """
    Determine the best match for timezone.
    """
    # 1. Timezone from URL parameters
    timezone = request.args.get('timezone')
    if timezone:
        try:
            # Validate the timezone
            pytz.timezone(timezone)
            return timezone
        except UnknownTimeZoneError:
            pass

    # 2. Timezone from user settings
    user = g.get('user', None)
    if user and user['timezone']:
        try:
            # Validate the timezone
            pytz.timezone(user['timezone'])
            return user['timezone']
        except UnknownTimeZoneError:
            pass

    # 3. Default timezone
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def home():
    """ A simple / route """
    return render_template('7-index.html')


if __name__ == '__main__':
    """ Main Function """
    app.run(debug=True)
