#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    return (jsonify({"status": "OK"}))


@app_views.route('/stats')
def count():
    cls = ["Amenity", "City", "Place", "Review", "State", "User"]
    count = []
    for i in cls:
        objects = storage.count(i)
        count.append(objects)
    cls_count = jsonify(
        {
            "amenities": count[0],
            "cities": count[1],
            "places": count[2],
            "reviews": count[3],
            "states": count[4],
            "users": count[5]
        })
    return cls_count
