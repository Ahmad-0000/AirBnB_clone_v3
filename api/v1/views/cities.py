#!/usr/bin/python3
"""Cities blueprint"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/states/<uuid:state_id>/cities", strict_slashes=False)
def cities_by_state(state_id):
    """Reterive all cities of the state with id equal to state_id"""
    from models import storage
    from models.state import State
    from models.city import City

    state = storage.get(State, str(state_id))
    if not state:
        abort(404)
    cities = state.cities
    return make_response(jsonify([city.to_dict() for city in cities]), 200)


@app_views.route("/cities", strict_slashes=False)
def all_cities():
    """Reterive all cities from storage"""
    from models import storage
    from models.city import City

    cities_dict = storage.all(City)
    cities_list = []
    for city in cities_dict.values():
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route("/cities/<uuid:city_id>", strict_slashes=False)
def one_city(city_id):
    """Reterive one city from storage"""
    from models import storage
    from models.city import City

    one_city = storage.get(City, str(city_id))
    if one_city:
        return jsonify(one_city.to_dict())
    abort(404)


@app_views.route("/cities/<uuid:city_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """Delete city from the storage"""
    from models import storage
    from models.city import City

    city = storage.get(City, str(city_id))
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<uuid:state_id>/cities", strict_slashes=False,
                 methods=['POST'])
def add_city(state_id):
    """Add new city in the storage"""
    from models import storage
    from models.city import City
    from models.state import State

    state = storage.get(State, str(state_id))
    if not state:
        abort(404)
    if request.is_json:
        request_data = request.get_json()
        if "name" in request_data:
            new_city = City(**request_data)
            new_city.__dict__['state_id'] = str(state_id)
            new_city.save()
            return make_response(jsonify(new_city.to_dict()), 201)
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route("/cities/<uuid:city_id>", strict_slashes=False,
                 methods=['PUT'])
def update_city_info(city_id):
    """Updating city info"""
    from models import storage
    from models.city import City

    city = storage.get(City, str(city_id))
    if not city:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    update_data = request.get_json()
    for key, value in update_data.items():
        if key == "state_id" or key == "id" or key == "created_at"\
                or key == "updated_at":
            continue
        city.__dict__[key] = value
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
