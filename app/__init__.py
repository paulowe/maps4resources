import os, sys
from flask import Flask, g, abort
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_assets import Environment
from flask_wtf import CsrfProtect
from flask_compress import Compress
from flask_rq import RQ
from functools import wraps
from config import config
from .assets import app_css, app_js, vendor_css, vendor_js

basedir = os.path.abspath(os.path.dirname(__file__))

mail = Mail()
db = SQLAlchemy()
csrf = CsrfProtect()
compress = Compress()
# Set up Flask-Login
login_manager = LoginManager()
# TODO: Ideally this should be strong, but that led to bugs. Once this is
# fixed, switch protection mode back to 'strong'
login_manager.session_protection = 'basic'
# @Paul: This is the view that a non authenticated user will get redirected to
login_manager.login_view = 'account.login'

# write everything in the buffer to the terminal
def pf(*args, **kwds):
    print (*args, **kwds)
    sys.stdout.flush()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    #Set up extensions.
    ''' 
    @Paul: init_app(app) binds each instance of the respective 
    application to the flask app. However, we do no need to specify
    an application context while using things like db, mail, login_manager
    since they are not bound to our application exclusively. 
    '''
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    compress.init_app(app)
    RQ(app)

    # Register Jinja template functions
    from .utils import register_template_utils
    register_template_utils(app)

    # Set up asset pipeline
    assets_env = Environment(app)
    dirs = ['assets/styles', 'assets/scripts']
    for path in dirs:
        assets_env.append_path(os.path.join(basedir, path))
    assets_env.url_expire = True

    assets_env.register('app_css', app_css)
    assets_env.register('app_js', app_js)
    assets_env.register('vendor_css', vendor_css)
    assets_env.register('vendor_js', vendor_js)

    # Configure SSL if platform supports it
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        SSLify(app)

    # Create app blueprints
    # @Paul - blueprints allow us to set url prefixes for routes contained within the views file
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .account import account as account_blueprint
    app.register_blueprint(account_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .bulk_resource import bulk_resource as bulk_resource_blueprint
    app.register_blueprint(bulk_resource_blueprint)

    from .descriptor import descriptor as descriptor_blueprint
    app.register_blueprint(descriptor_blueprint)

    from .single_resource import single_resource as single_resource_blueprint
    app.register_blueprint(single_resource_blueprint)

    from .suggestion import suggestion as suggestion_blueprint
    app.register_blueprint(suggestion_blueprint)

    from .contact import contact as contact_blueprint
    app.register_blueprint(contact_blueprint)

    
    '''
    @paulowe: Check paths
    '''
    
    @app.before_request
    def br():
        from flask import request
        g.tlf = request.path[1:].split('/',1)[0] 

        from .models import Locale
        Locale.check_locale(g.tlf)

    
    @app.after_request
    def ar(response):
        # if not tlf(g.tlf)
        pass #abort(404)
        return response
    return app


