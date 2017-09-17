#!/usr/bin/python3
""" This module handles all default RESTful API actions """
from flask import abort, jsonify, request
from models import storage
from models.base_model import *
from models.amenity import Amenity
from models.place import Place, PlaceAmenity
from models.engine.db_storage import DBStorage
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def place_amenity_get(place_id):
    """
    list all objects
    """
    new_list = []

    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    for value in place.amenities:
        json_val = value.to_json()
        new_list.append(json_val)
    return (jsonify(new_list))


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def place_amenity_delete(place_id, amenity_id):
    """
    delete amenity object from place
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    empty_dict = {}
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    try:
        for value in place.amenities:
            if value.id == amenity_id:
                place.amenities.remove(value)
                storage.save()
        return(jsonify(empty_dict))
    except:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def place_amenity_post(place_id, amenity_id):
    """
    create amenity object from place
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return (jsonify(amenity.to_json()))
    place.amenities.append(amenity)
    storage.save()
    return (jsonify(amenity.to_json()), 201)
