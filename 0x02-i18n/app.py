#!/usr/bin/env python3
'''Display the current time
'''
import pytz
from typing import Union, Dict
from flask_babel import Babel, format_datetime
from flask import Flask, render_template, request, g


class Config:
    '''Represents a Flask Babel configuration.
    '''
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict, None]:
    '''Retrieves a user id.
    '''
    login_id = request.args.get('login_as', '')
    if login_id:
        return users.get(int(login_id), None)
    return None


@app.before_request
def before_request() -> None:
    '''Performs request's resolution.
    '''
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale() -> str:
    '''Retrieves the locale for a web page.
    '''
    queries = request.query_string.decode('utf-8').split('&')
    query_table = dict(map(
        lambda x: (x if '=' in x else '{}='.format(x)).split('='),
        queries,
    ))
    locale = query_table.get('locale', '')
    if locale in app.config["LANGUAGES"]:
        return locale
    user_data = getattr(g, 'user', None)
    if user_data and user_data['locale'] in app.config["LANGUAGES"]:
        return user_data['locale']
    locale_header = request.headers.get('locale', '')
    if locale_header in app.config["LANGUAGES"]:
        return locale_header
    return app.config['BABEL_DEFAULT_LOCALE']


@babel.timezoneselector
def get_timezone() -> str:
    '''Retrieves the timezone for a web page.
    '''
    timezone = request.args.get('timezone', '').strip()
    if not timezone and g.user:
        timezone = g.user['timezone']
    try:
        return pytz.timezone(timezone).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def get_index() -> str:
    '''The index page.
    '''
    g.time = format_datetime()
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
