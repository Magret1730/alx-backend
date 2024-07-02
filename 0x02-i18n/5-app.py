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

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """
    Returns a user dictionary or None if the ID cannot be found or if login_as
    was not passed.
    """
    try:
        user_id = int(request.args.get('login_as'))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """ Set g.user before each request"""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """
    Determine the best match with our supported languages.
    """
    user = g.get('user', None)
    if user and user['locale'] in app.config['LANGUAGES']:
        return user['locale']

    # Check if the locale parameter is present in the request args
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    # Fallback to the best match from the request accept languages
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def home():
    """ A simple / route """
    return render_template('5-index.html')


if __name__ == '__main__':
    """ Main Function """
    app.run(debug=True)
