#!/usr/bin/python3
""" This module handles all default RESTful API actions """
from flask import abort, jsonify, request
from models import storage
from models.base_model import *
from models.state import State
from models.engine.db_storage import DBStorage
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'])
def state_get():
    """
    get list of all states
    """
    new_list = []
    states = storage.all("State").items()

    for key, value in states:
        json_val = value.to_json()
        new_list.append(json_val)
    return (jsonify(new_list))


@app_views.route('/states/<state_id>', methods=['GET'])
def state_get_id(state_id):
    """
    get state which matches id
    """
    states = storage.all("State").items()
    for key, value in states:
        if state_id == value.id:
            json_val = value.to_json()
            return (jsonify(json_val))
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def state_delete(state_id):
    """
    delete state which matches id
    """
    states = storage.all("State").items()
    empty_dict = {}
    for key, value in states:
        if state_id == value.id:
            storage.delete(value)
            storage.save()
            return (jsonify(empty_dict))
    abort(404)


@app_views.route('/states', methods=['POST'])
def state_post():
    """
    creates new state object instance
    """
    new_state = State()

    req = request.get_json()
    if req is None:
        return ("Not a JSON", 400)
    if 'name' not in req.keys():
        return ("Missing name", 400)

    new_state.__dict__.update(req)
    new_state.save()
    return (jsonify(new_state.to_json()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def state_put(state_id):
    """
    updates dictionary
    """
    req = request.get_json()
    if req is None:
        return ("Not a JSON", 400)
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    skip = ['id', 'created_at', 'updated_at', '_sa_instance_state']
    for i in state.__dict__:
        if i not in skip:
            setattr(state, i, req[i])

    state.save()
    return (jsonify(state.to_json()))
