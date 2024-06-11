#!/usr/bin/python3
"""States blueprint"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/amenities", strict_slashes=False)
def all_amenitites():
    """Reterive all cities from storage"""
    from models import storage
    from models.amenity import Amenity

    states_dict = storage.all(Amenity)
    states_list = []
    for state in states_dict.values():
        states_list.append(state.to_dict())
    return jsonify(states_list)

@app_views.route("/amenities/<uuid:city_id>", strict_slashes=False)
def one_amenity(city_id):
    """Reterive one city from storage"""
    from models import storage
    from models.amenity import Amenity

    one_state = storage.get(Amenity, str(city_id))
    if one_state:
        return jsonify(one_state.to_dict())
    abort(404)

@app_views.route("/amenities/<uuid:city_id>", strict_slashes=False, methods=['DELETE'])
def delete_amenity(city_id):
    """Delete city from the storage"""
    from models import storage
    from models.amenity import Amenity

    state = storage.get(Amenity, str(city_id))
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})

#@app_views.route("/states", strict_slashes=False, methods=['POST'])
#def add_city():
#    """Add new state in the storage"""
#    from models import storage
#    from models.amenity import State

#    if not requsest.json:
#        make_response(jsonify())
