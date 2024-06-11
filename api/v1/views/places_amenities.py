#!/usr/bin/python3
"""Reviews blueprint"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/places/<uuid:place_id>/amenities", strict_slashes=False)
def place_amenities(place_id):
    """Reterive all amenities of a place"""
    from models import storage
    from models.place import Place

    place = storage.get(Place, str(place_id))
    if not place:
        abort(404)
    amenities = place.amenities
    return make_response(jsonify([amenity.to_dict() for amenity in amenities]),
                         200)


@app_views.route("/places/<uuid:place_id>/amenities/<uuid:amenity_id>",
                 strict_slashes=False, methods=['DELETE'])
def remove_amenity(place_id, amenity_id):
    """Delete amenity of a place"""
    from models import storage, storage_t
    from models.place import Place
    from models.amenity import Amenity

    place = storage.get(Place, str(place_id))
    if not place:
        abort(404)
    amenity = storage.get(Amenity, str(amenity_id))
    if not amenity:
        abort(404)
    if storage_t == "db":
        if amenity not in place.amenities:
            abort(404)
        else:
            place.amenities.remove(amenity)
            storage.save()
    else:
        if amenity.id not in place.amenity_ids:
            abort(404)
        else:
            place.amenity_ids.remove(amenity.id)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<uuid:place_id>/amenities/<uuid:amenity_id>",
                 strict_slashes=False, methods=['POST'])
def new_amenity(place_id, amenity_id):
    """Add a new amenity to a place"""
    from models import storage, storage_t
    from models.place import Place
    from models.amenity import Amenity

    place = storage.get(Place, str(place_id))
    if not place:
        abort(404)
    amenity = storage.get(Amenity, str(amenity_id))
    if not amenity:
        abort(404)
    if amenity in place.amenities:
        return make_response(jsonify(amenity.to_dict()), 200)
    if storage_t == "db":
        place.amenities.append(amenity)
        storage.save()
    else:
        place.amenity_ids.append(amenity.id)
        amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)
