#!/usr/bin/python3
"""States blueprint"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/cities", strict_slashes=False)
def all_cities():
    """Reterive all cities from storage"""
    from models import storage
    from models.city import City

    states_dict = storage.all(City)
    states_list = []
    for state in states_dict.values():
        states_list.append(state.to_dict())
    return jsonify(states_list)

@app_views.route("/cities/<uuid:city_id>", strict_slashes=False)
def one_city(city_id):
    """Reterive one city from storage"""
    from models import storage
    from models.city import City

    one_state = storage.get(City, str(city_id))
    if one_state:
        return jsonify(one_state.to_dict())
    abort(404)

@app_views.route("/cities/<uuid:city_id>", strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """Delete city from the storage"""
    from models import storage
    from models.city import City

    state = storage.get(City, str(city_id))
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})

#@app_views.route("/states", strict_slashes=False, methods=['POST'])
#def add_city():
#    """Add new state in the storage"""
#    from models import storage
#    from models.state import State

#    if not requsest.json:
#        make_response(jsonify())
