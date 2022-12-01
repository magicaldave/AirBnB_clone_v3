#!/usr/bin/python3
"""
Module to create State views
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route("/states/", methods=["GET"],
                 strict_slashes=False)
def state_get():
    """
    Retrieves all states
    """
    all_states = storage.all(State)
    states_list = []
    for state in all_states.values():
        states_list.append(state.to_dict())
    return make_response(jsonify(states_list))


@app_views.route("/states/<state_id>", methods=["GET"],
                 strict_slashes=False)
def state_id_get(state_id):
    """
    Retrieves a specified state
    Or 404 if not matched.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return make_response(jsonify(state.to_dict()))


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_id_delete(state_id):
    """
    Deletes a specific state ID.
    Raise 404 if not matched.
    Otherwise, return an empty dict with status 200
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/", methods=["POST"],
                 strict_slashes=False)
def state_post():
    """
    Create a State with POST request.
    Raise "400 - Not a JSON" if the HTTP body isn't valid JSON.
    If the dict doesn't match the key name, raise "400 - missing Message Name"
    Otherwise, return new State with code 201.
    """
    request_dict = request.get_json(silent=True)
    if request_dict is not None:
        if 'name' in request_dict.keys() and request_dict['name'] is not None:
            new_state = State(**request_dict)
            new_state.save()
            return make_response(jsonify(new_state.to_dict()), 201)
        return make_response(jsonify({'error': 'Missing name'}), 400)
    return make_response(jsonify({'error': 'Not a JSON'}), 400)


@app_views.route("/states/<state_id>", methods=["PUT"],
                 strict_slashes=False)
def state_put(state_id):
    """
    Updates a State with PUT.
    Raise 404 if the ID is unmatched.
    If the HTTP body is invalid JSON, raise "400 - Not a JSON"
    Update the state with all keypairs in the dict
    Ignore the id and creation/updated times.
    """
    state = storage.get(State, state_id)
    if state is None:
            abort(404)
    if request.get_json() is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
    content = request.get_json()
    ignore_keys = ["id", "created_at", "updated_at"]
    for k, v in content.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
