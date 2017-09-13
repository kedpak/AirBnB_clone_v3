from api.v1.views import app_views
from flask import jsonify
from models  import storage


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
    cls_count = jsonify({"amenities": objects, 
            "cities": count[0],
            "places": count[1],
            "reviews": count[2],
            "states": count[3],
            "users": count[4]
            })
    return cls_count
