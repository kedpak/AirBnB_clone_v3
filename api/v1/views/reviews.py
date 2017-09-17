#!/usr/bin/python3
""" This module handles all default RESTful API actions """
from flask import abort, jsonify, request
from models import storage
from models.base_model import *
from models.review import Review
from models.engine.db_storage import DBStorage
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def review_get(place_id):
    """
    get list of all states
    """
    new_list = []
    review = storage.all("Review").items()
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    for key, value in review:
        json_val = value.to_json()
        new_list.append(json_val)
    return (jsonify(new_list))


@app_views.route('/reviews/<review_id>', methods=['GET'])
def review_get_id(review_id):
    """
    get state which matches id
    """
    review = storage.all("Review").items()
    flag = 0
    for i, j in review:
        if review_id == j.id:
            flag = 1
    if flag == 0:
        abort(404)
    for key, value in review:
        if review_id == value.id:
            json_val = value.to_json()
            return (jsonify(json_val))
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def review_delete(review_id):
    """
    delete state which matches id
    """
    review = storage.all("Review").items()
    empty_dict = {}
    flag = 0

    for i, j in review:
        if review_id == j.id:
            flag = 1
    if flag == 0:
        abort(404)
    for key, value in review:
        if review_id == value.id:
            storage.delete(value)
            storage.save()
            return (jsonify(empty_dict))
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def review_post(place_id):
    """
    creates new state object instance
    """
    new_review = Review()

    req = request.get_json()

    place = storage.get("Place", place_id)
    if place is None:
        aboart(404)
    user = storage.get("User", req.get("user_id"))
    if user is None:
        abort(404)
    if req is None:
        return ("Not a JSON", 400)
    if 'user_id' not in req.keys():
        return ("Missing user_id", 400)
    if 'text' not in req.keys():
        return ("Missing test", 400)

    req["place_id"] = place_id
    new_review.__dict__.update(req)
    new_review.save()
    return (jsonify(new_review.to_json()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def review_put(review_id):
    """
    updates dictionary
    """
    req = request.get_json()

    if req is None:
        return ("Not a JSON", 400)
    review = storage.get('Review', review_id)

    if review is None:
        abort(404)
    flag = 0
    for i, j in storage.all("Review").items():
        if review_id == j.id:
            flag = 1
    if flag == 0:
        abort(404)

    skip = [
        'id',
        'created_at',
        'updated_at',
        'user_id',
        'place_id',
        '_sa_instance_state']

    for i in review.__dict__:
        if i not in skip and i in req:
            setattr(review, i, req[i])

    review.save()
    return (jsonify(review.to_json()))
