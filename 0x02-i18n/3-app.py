#!/usr/bin/env python3
"""
Basic Flask app with Babel app, language selector, and parameterized templates
"""

from flask import Flask, render_template
from flask_babel import Babel

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
def get_locale():
    """
    Determne the best match for the user's preferred language
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """
    Route to render index.html template with parameterized messages
    """
    return render_template('3-index.html',
                            home_title=gettest("Welcome to Holberton"),
                            home_header=gettest("Hello world"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port"5000")