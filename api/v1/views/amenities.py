#!/usr/bin/python3
"""Amenity blueprint"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/amenities", strict_slashes=False)
def all_amenities():
    """Reterive all amenities from storage"""
    from models import storage
    from models.amenity import Amenity

    amenities_dict = storage.all(Amenity)
    amenities_list = []
    for amenity in amenities_dict.values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route("/amenities/<uuid:amenity_id>", strict_slashes=False)
def one_amenity(amenity_id):
    """Reterive one amenity from storage"""
    from models import storage
    from models.amenity import Amenity

    amenity = storage.get(Amenity, str(amenity_id))
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<uuid:amenity_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """Delete one amenity from storage"""
    from models import storage
    from models.amenity import Amenity

    amenity = storage.get(Amenity, str(amenity_id))
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route("/amenities", strict_slashes=False, methods=['POST'])
def add_amenity():
    """Add new amentiy to storage"""
    from models.amenity import Amenity

    if not request.is_json:
        abort(400, "Not a JSON")
    request_data = request.get_json()
    if "name" not in request_data:
        abort(400, "Missing name")
    new_amenity = Amenity(**request_data)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route("/amenities/<uuid:amenity_id>", strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """Update amentiy info"""
    from models import storage
    from models.amenity import Amenity

    amenity = storage.get(Amenity, str(amenity_id))
    if not amenity:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    request_data = request.get_json()
    for k, v in request_data.items():
        if k == "id" or k == "updated_at" or k == "created_at":
            continue
        amenity.__dict__[k] = v
    amenity.save()
    return jsonify(amenity.to_dict())
