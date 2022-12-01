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
