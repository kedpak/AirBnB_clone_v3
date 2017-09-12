#!/usr/bin/python3
""" This module handles all default RESTful API actions """
from flask import abort, jsonify, request
from models import storage
from models.base_model import *
from models.state import State
from models.engine.db_storage import DBStorage
from api.v1.views import app_views

@app_views.route('/states', methods=['GET'])
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'])
def states(state_id=None):

    new_list = []
    empty_dict = {}
    states = storage.all("State").items()

    for key, value in states:
        if request.method == 'GET':
            if state_id is not None:
                if state_id == value.id:
                    json_val = value.to_json()
                    return (jsonify(json_val))
                else:
                    abort(404)

            else:
                json_val = value.to_json()
                new_list.append(json_val)

        if request.method == 'DELETE':
            if state_id is not None:
                if state_id == value.id:
                    storage.delete(value)
                    storage.save()
                    return (jsonify(empty_dict))
                else:
                    abort(404)

    return (jsonify(new_list))
