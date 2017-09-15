#!/usr/bin/python3
""" This module handles all default RESTful API actions """
from flask import abort, jsonify, request
from models import storage
from models.base_model import *
from models.user import User
from models.engine.db_storage import DBStorage
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'])
def user_get():
    """
    get list of all states
    """
    new_list = []
    user = storage.all("User").items()

    for key, value in user:
        json_val = value.to_json()
        new_list.append(json_val)
    return (jsonify(new_list))


@app_views.route('/users/<user_id>', methods=['GET'])
def user_get_id(user_id):
    """
    get state which matches id
    """
    user = storage.all("User").items()
    for key, value in user:
        if user_id == value.id:
            json_val = value.to_json()
            return (jsonify(json_val))
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def user_delete(user_id):
    """
    delete state which matches id
    """
    user = storage.all("User").items()
    empty_dict = {}
    for key, value in user:
        if user_id == value.id:
            storage.delete(value)
            storage.save()
            return (jsonify(empty_dict))
    abort(404)


@app_views.route('/users', methods=['POST'])
def user_post():
    """
    creates new state object instance
    """
    new_user = User()

    req = request.get_json()
    if req is None:
        return ("Not a JSON", 400)
    if 'email' not in req.keys():
        return ("Missing email", 400)
    if 'password' not in req.keys():
        return ("Missing password", 400)

    new_user.__dict__.update(req)
    new_user.save()
    return (jsonify(new_user.to_json()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def user_put(user_id):
    """
    updates dictionary
    """
    req = request.get_json()
    if req is None:
        return ("Not a JSON", 400)
    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    skip = ['id', 'email', 'created_at', 'updated_at', '_sa_instance_state']
    for i in user.__dict__:
        if i not in skip:
            setattr(user, i, req[i])

    user.save()
    return (jsonify(user.to_json()), 200)
