#!/usr/bin/python3
""" This module handles all default RESTful API actions """
from flask import abort, jsonify, request
from models import storage
from models.base_model import *
from models.place import Place
from models.engine.db_storage import DBStorage
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def place_get(city_id):
    """
    get list of all places
    """
    new_list = []
    place = storage.all("Place").items()
    flag1 = 0
    for i, j in storage.all("City").items():
        if city_id == j.id:
            flag1 = 1
    if flag1 == 0:
        abort(404)
    for key, value in place:
        if city_id == value.city_id:
            json_val = value.to_json()
            new_list.append(json_val)
    return (jsonify(new_list))


@app_views.route('/places/<place_id>', methods=['GET'])
def place_get_id(place_id):
    """
    get place which matches id
    """
    place = storage.all("Place").items()
    for key, value in place:
        if place_id == value.id:
            json_val = value.to_json()
            return (jsonify(json_val))
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def place_delete(place_id):
    """
    delete place which matches id
    """
    place = storage.all("Place").items()
    empty_dict = {}
    for key, value in place:
        if place_id == value.id:
            storage.delete(value)
            storage.save()
            return (jsonify(empty_dict))
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def place_post(city_id):
    """
    creates new place object instance
    """
    new_place = Place()

    req = request.get_json()

    city = storage.get("City", city_id)

    if city is None:
        abort(404)
    if req is None:
        return ("Not a JSON", 400)
    if 'user_id' not in req.keys():
        return ("Missing email", 400)
    if 'name' not in req.keys():
        return ("Missing password", 400)

    user = storage.get("User", req.get("user_id"))
    if user is None:
        abort(404)

    req["city_id"] = city_id
    new_place.__dict__.update(req)
    new_place.save()
    return (jsonify(new_place.to_json()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def place_put(place_id):
    """
    updates dictionary
    """
    req = request.get_json()
    if req is None:
        return ("Not a JSON", 400)
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    skip = [
        'id',
        'user_id',
        'city_id'
        'created_at',
        'updated_at',
        '_sa_instance_state']

    for i in place.__dict__:
        if i not in skip and i in req:
            setattr(place, i, req[i])

    place.save()
    return (jsonify(place.to_json()), 200)
