# Licensed Materials - Property of IBM
# 5725I71-CC011829
# (C) Copyright IBM Corp. 2015, 2020. All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.

__author__ = "IBM"

from packaging import version

import secrets  # For generating a new secret key
from flask_wtf.csrf import CSRFProtect  # To add CSRF protection
from qpylib.encdec import (
    Encryption,
    EncryptionError,
)  # To handle storing the secret key securely

from flask import Flask
from qpylib import qpylib, log_qpylib, __version__


def suppress_syslog():
    return None


# Flask application factory.
def create_app():
    # Create a Flask instance.
    qflask = Flask(__name__)

    csrf = CSRFProtect()
    csrf.init_app(qflask)

    # Generate or retrieve a secret key
    try:
        # Read in secret key
        secret_key_store = Encryption({"name": "secret_key", "user": "shared"})
        secret_key = secret_key_store.decrypt()
    except EncryptionError:
        # If secret key file doesn't exist/fail to decrypt it,
        # generate a new random password for it and encrypt it
        secret_key = secrets.token_urlsafe(64)
        secret_key_store = Encryption({"name": "secret_key", "user": "shared"})
        secret_key_store.encrypt(secret_key)

    qflask.config["SECRET_KEY"] = secret_key

    # Retrieve QRadar app id.
    qradar_app_id = qpylib.get_app_id()

    # Create unique session cookie name for this app.
    qflask.config["SESSION_COOKIE_NAME"] = "session_{0}".format(qradar_app_id)

    # Hide server details in endpoint responses.
    # pylint: disable=unused-variable
    @qflask.after_request
    def obscure_server_header(resp):
        resp.headers["Server"] = "QRadar App {0}".format(qradar_app_id)
        return resp

    # Register q_url_for function for use with Jinja2 templates.
    qflask.add_template_global(qpylib.q_url_for, "q_url_for")

    # Initialize logging.
    if version.parse(__version__) >= version.parse("2.0.5"):
        qpylib.create_log(False)
    else:
        log_qpylib._get_address_for_syslog = suppress_syslog
        qpylib.create_log()

    # To enable app health checking, the QRadar App Framework
    # requires every Flask app to define a /debug endpoint.
    # The endpoint function should contain a trivial implementation
    # that returns a simple confirmation response message.
    @qflask.route("/debug")
    def debug():
        return "Pong!"

    # Import additional endpoints.
    # For more information see:
    #   https://flask.palletsprojects.com/en/1.1.x/tutorial/views
    from . import views

    qflask.register_blueprint(views.viewsbp)
    from . import dev

    qflask.register_blueprint(dev.devbp)

    return qflask
