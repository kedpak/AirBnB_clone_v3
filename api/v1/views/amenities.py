#!/usr/bin/python3
""" This module handles all default RESTful API actions """
from flask import abort, jsonify, request
from models import storage
from models.base_model import *
from models.state import State
from models.amenity import Amenity
from models.engine.db_storage import DBStorage
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'])
def amenity_get():
    """
    get list of all amenities
    """
    new_list = []
    amenities = storage.all("Amenity").items()

    for key, value in amenities:
        json_val = value.to_json()
        new_list.append(json_val)
    return (jsonify(new_list))


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenity_get_id(amenity_id):
    """
    get amenity which matches id
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    json_val = amenity.to_json()
    return (jsonify(json_val))


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def amenity_delete(amenity_id):
    """
    delete amenity which matches id
    """
    amenity = storage.get("Amenity", amenity_id)

    if amenity is None:
        abort(404)

    empty_dict = {}
    if amenity_id == amenity.id:
        storage.delete(amenity)
        storage.save()
        return (jsonify(empty_dict))


@app_views.route('/amenities', methods=['POST'])
def amenity_post():
    """
    creates new amenity object instance
    """
    new_amenity = Amenity()

    req = request.get_json()
    if req is None:
        return ("Not a JSON", 400)
    if 'name' not in req.keys():
        return ("Missing name", 400)

    new_amenity.__dict__.update(req)
    new_amenity.save()
    return (jsonify(new_amenity.to_json()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def amenity_put(amenity_id):
    """
    updates dictionary of existing Amenity object,
    which matches given amenity_id
    """
    req = request.get_json()
    if req is None:
        return ("Not a JSON", 400)
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)

    skip = ['id', 'created_at', 'updated_at', '_sa_instance_state']
    for i in amenity.__dict__:
        if i not in skip:
            setattr(amenity, i, req[i])

    amenity.save()
    return (jsonify(amenity.to_json()))
