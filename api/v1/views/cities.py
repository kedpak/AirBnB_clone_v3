#!/usr/bin/python3
""" This module handles all default RESTful API actions """
from flask import abort, jsonify, request
from models import storage
from models.base_model import *
from models.state import State
from models.city import City
from models.engine.db_storage import DBStorage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def cities_get(state_id=None):
    """
    get list of all cities in a given state
    """
    state = storage.get("State", state_id)

    if state is None:
        abort(404)
    else:
        new_list = []
        for city in state.cities:
            json_val = city.to_json()
            new_list.append(json_val)
        return (jsonify(new_list))


@app_views.route('/cities/<city_id>', methods=['GET'])
def cities_get_id(city_id=None):
    """
    get city which matches given id
    """

    city = storage.get("City", city_id)

    if city is None:
        abort(404)
    if city_id == city.id:
        json_val = city.to_json()
        return (jsonify(json_val))
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def city_delete(city_id):
    """
    delete city which matches given id
    """
    city = storage.get("City", city_id)

    if city is None:
        abort(404)

    empty_dict = {}
    if city_id == city.id:
        storage.delete(city)
        storage.save()
        return (jsonify(empty_dict))


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def city_post(state_id=None):
    """
    creates new city object instance
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    new_city = City()
    req = request.get_json()
    req['state_id'] = state_id

    if req is None:
        return ("Not a JSON", 400)
    if 'name' not in req.keys():
        return ("Missing name", 400)

    new_city.__dict__.update(req)
    new_city.save()
    return (jsonify(new_city.to_json()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def city_put(city_id):
    """
    updates existing city object which matches given id
    """
    req = request.get_json()
    if req is None:
        return ("Not a JSON", 400)

    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    skip = ['id', 'created_at', 'updated_at', '_sa_instance_state']
    for i in city.__dict__:
        if i not in skip and i in req:
            setattr(city, i, req[i])
    city.save()
    return (jsonify(city.to_json()))
