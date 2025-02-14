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
    if not state:
        abort(404)
    for city in state.cities:
        cities_list.append(city.to_dict())
    return make_response(jsonify(cities_list))


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Gets a city object.
    GET /api/v1/cities/<city_id>
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return make_response(jsonify(city.to_dict()))


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def del_city(city_id):
    """
    Deletes a city object.
    DELETE /api/v1/cities/<city_id>
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities/', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Creates a city object.
    POST /api/v1/states/<state_id>/cities
    """
    state = storage.get(State, state_id)
    content = request.get_json()
    if not state:
        abort(404)
    if not content:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if 'name' not in content:
        return make_response(jsonify({'error': "Missing name"}), 400)
    new_city = City(**content)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>/', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Update a City object.
    PUT /api/v1/cities/<city_id>
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for k, v in request.get_json().items():
        if k not in ignore_keys:
            setattr(city, k, v)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
