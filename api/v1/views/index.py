#!/usr/bin/python3
"""Creates routes to API objects"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """Returns OK status"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def get_stats():
    """
    Endpoint that retrieves the number of ojbects of each
    type.
    """
    count_directory = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(count_directory)
