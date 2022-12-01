#!/usr/bin/python3
"""
Create an API interface for City objects
"""

from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities(state_id):
    """
    Gets all Cities of a State
    GET /api/v1/states/<state_id>/cities
    """
    cities_list = []
    state = storage.get(State, state_id)
    if not s_id:
        abort(404)
    for city in storage.all(City).values():
        if city.state_id == state_id:
            cities_list.append(city.to_dict())
    return make_response(jsonify(cities_list), 200)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Gets a city object.
    GET /api/v1/cities/<city_id>
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return make_response(jsonify(city.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def del_city(city_id):
    """
    Deletes a city object.
    DELETE /api/v1/cities/<city_id>
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)
