#!/usr/bin/python
"""
Creates an API view for Amenities.
"""

from models.amenity import Amenity
from models import storage
from flask import request, abort, make_response
from api.v1.views import app_views


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """
    POSTs an Amenity.
    /api/v1/amenities
    """
    if not request.get_json():
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': "Missing name"}), 400)
    content = request.get_json()
    new_amenity = Amenity(**content)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """
    PUTs an amenity (updates it)
    /api/v1/amenities/<amenity_id>
    """
    content = request.get_json(silent=True)
    ignored = ['id', 'created_at', 'updated_at']
    if content is not None:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        for k, v in content.items():
            if key not in ignored:
                setattr(amenity, k, v)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
    return make_response(jsonify({'error': "Not a JSON"}), 400)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def amenity_id_delete(amenity_id):
    """
    Deletes a specific amenity.
    Raise 404 if unmatched, otherwise return empty dict with status 200.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities/", methods=["GET"],
                 strict_slashes=False)
def amenities_get():
    """
    Retrieves all amenities
    """
    all_amenities = storage.all(Amenity)
    amenity_list = []
    for amenity in all_amenities.values():
        amenity_list.appent(amenity.to_dict())
    return make_response(jsonify(amenity_list), 200)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def amenity_id_get(amenity_id):
    """
    Retrieves a specified amenity.
    Raises 404 if unmatched
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return make_response(jsonify(amenity.to_dict()), 200)
