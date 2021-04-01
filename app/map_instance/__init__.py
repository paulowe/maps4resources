from flask import Blueprint, g

map_instance = Blueprint('map_instance', __name__, url_prefix='/<tlf>/map_instance')

@map_instance.url_defaults
def add_locale(endpoint, values):
    values.setdefault('tlf',g.tlf)

@map_instance.url_value_preprocessor
def pull_locale(endpoint, values):
    g.tlf = values.pop('tlf')

from . import views  # noqa
