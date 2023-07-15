# Licensed Materials - Property of IBM
# 5725I71-CC011829
# (C) Copyright IBM Corp. 2015, 2020. All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.

import ipaddress
import requests


from flask import Blueprint, render_template, current_app, send_from_directory, request, redirect, jsonify, abort
from qpylib.encdec import Encryption
from qpylib import qpylib

# pylint: disable=invalid-name

viewsbp = Blueprint('viewsbp', __name__, url_prefix='/')
SecretStore = Encryption({"name": "crowdsec_config", "user": "crowdsec"})

def get_api_key():
    try:
        return SecretStore.decrypt()
    except:
        return ""


# The presence of this endpoint avoids a Flask error being logged when a browser
# makes a favicon.ico request. It demonstrates use of send_from_directory
# and current_app.
@viewsbp.route('/favicon.ico')
def favicon():
    return send_from_directory(current_app.static_folder, 'favicon-16x16.png')


@viewsbp.route("/updateConfig", methods=["POST"])
def update_config():
    api_key = request.form["api-key"]
    SecretStore.encrypt(api_key)
    return redirect(qpylib.q_url_for("viewsbp.config"), code=303)


@viewsbp.route("/config")
def config():
    """Render app configuration page."""
    api_key= "*" * len(get_api_key())
    return render_template("config.html", api_key=api_key)

@viewsbp.route("/right_click_ip",  methods=["GET"])
def right_click_ip():
    ip = request.args.get("context")
    try:
        ipaddress.ip_address(ip)
    except Exception as e:
        return abort(500)

    return jsonify({"ip": ip, "base_url": qpylib.get_app_base_url()})

@viewsbp.route("/smoke")
def lookup_in_smoke():
    ip = request.args.get('context')
    api_key = get_api_key()
    resp = requests.get(
        f"https://cti.api.crowdsec.net/v2/smoke/{ip}",
        headers={"x-api-key": api_key,
                "User-Agent": "crowdsec-qradar/v1.0.0",
                }
        )
    try:
        resp.raise_for_status()
    except Exception as e:
        error_msg=str(e)[3:]
        if resp.status_code == 429:
            error_msg = "Quota exceeded for CrowdSec CTI API. Please visit https://www.crowdsec.net/pricing to upgrade your plan."
        return render_template("error.html",ip=(ip),error_msg=error_msg, status=str(e)[:3], api_resp=resp.json())
    return render_template("smoke.html", data=resp.json())

