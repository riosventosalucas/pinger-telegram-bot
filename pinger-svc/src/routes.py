# -*- coding: utf-8 -*-

# Python

# Flask 
from flask import jsonify
from flask import request

# App
from config import app
from libs.pinger import *

@app.route('/', methods=['GET'])
@app.route('/ping', methods=['GET'])
def ping():
    return "Pong!"

@app.route('/api/v1/ip/check', methods=['GET'])
def ip_check():
    ip_address = request.args.get("ip")
    if get_ip_status(ip_address):
        return jsonify({"status": True})
    return jsonify({"status": False})