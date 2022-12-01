#!/usr/bin/python3
"""
Module to create State views
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_view.route("/states/", methods=["GET"],
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
