#!/usr/bin/env python3
"""
Basic Flask app with Babel app, language selector, and parameterized templates
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

app = Flask(__name__)
babel = Babel(app)


class Config:
    """
    Configration class for setting up Babel
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale() -> str:
    """
    Determne the best match for the user's preferred language
    """
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale

    user_locale = None
    if g.user:
        user_locale = g.user.get('locale')
        if user_locale and user_locale in app.config['LANGUAGES']:
            return user_locale

    header_locale = request.accept_languages.best_match(app.config['LANGUAGES'])
    if header_locale:
        return header_locale

    return app.config['BABEL_DEFAULT_LOCALE']


@app.route('/', strict_slashes=False)
def index():
    """
    Route to render index.html template with parameterized messages
    """
    return render_template('6-index.html')


def get_user(user_id):
    """
    Get user information based on user ID
    """
    return users.get(user_id)


@app.before_request
def before_request():
    """
    Executed before all other functions.
    sets the loogged in user as a global on flask.g.user
    """
    user_id = request.args.get('login_as')
    g.user = get_user(int(user_id)) if user_id else None


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
