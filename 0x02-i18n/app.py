#!/usr/bin/env python3
""" Flask App Initialization file """
from flask import Flask, render_template, g, request
from flask_babel import Babel, _

import pytz
from datetime import datetime
from pytz.exceptions import UnknownTimeZoneError

# Initialize app
app = Flask(__name__)


class Config:
    """ Config class for the languages and timezones """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


# Use Config to configure the app
app.config.from_object(Config)


# Initialize Babel
babel = Babel(app)

# Mock user database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """Retrieve user from the mock database based on login_as parameter."""
    user_id = request.args.get('login_as')
    if user_id and user_id.isdigit():
        return users.get(int(user_id))
    return None


@app.before_request
def before_request():
    """Set g.user before each request."""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """
    Determine the best match for locale.
    """
    # 1. Locale from URL parameters
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale

    # 2. Locale from user settings
    user = g.get('user', None)
    if user and user['locale'] in app.config['LANGUAGES']:
        return user['locale']

    # 3. Locale from request header
    return request.accept_languages.best_match(app.config['LANGUAGES'])


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
    # Get current time in the user's timezone
    timezone = get_timezone()
    current_time = datetime.now(pytz.timezone(timezone))

    # Format the current time for display
    formatted_time = current_time.strftime('%b %d, %Y, %I:%M:%S %p')

    return render_template('index.html', current_time=formatted_time)


if __name__ == '__main__':
    """ Main Function """
    app.run(debug=True)
