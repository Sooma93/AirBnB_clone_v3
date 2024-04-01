#!/usr/bin/python3
"""index.py to connect to API"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity


classes = {"amenities": Amenity,
           "cities": City,
           "places": Place,
           "reviews": Review,
           "states": State,
           "users": User
           }


@app_views.route('/status', strict_slashes=False)
def status():
    result = {
        "status": "OK"
    }
    return jsonify(result)


@app_views.route('/stats', strict_slashes=False)
def stats():
    """count stats"""
    dict = {}
    for key, value in classes.items():
        dict[key] = storage.count(value)
    return jsonify(dict)
