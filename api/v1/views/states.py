#!/usr/bin/python3
""" This module handles all default RESTful API actions """
from flask import request, jsonify
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET', 'POST', 'PUT', 'DELETE'])
def states():
    new_list = []
    if request.method == 'GET':
        for i, j in storage.all("State").items():
            j.to_json()
            new_list.append(j)
        return (j)
