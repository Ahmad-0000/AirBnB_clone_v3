#!/usr/bin/python3
"""Place blueprint"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def places_by_city(city_id):
    """Retrieve all places of a city"""
    from models import storage
    from models.city import City
    from models.place import Place

    city = storage.get(City, str(city_id))
    if not city:
        abort(404)
    places = city.places
    return jsonify([place.to_dict() for place in places])


@app_views.route("/places/<uuid:place_id>", strict_slashes=False)
def one_place(place_id):
    """Reterive one place account from storage"""
    from models import storage
    from models.place import Place

    place = storage.get(Place, str(place_id))
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<uuid:place_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_place_account(place_id):
    """Delete one place account from storage"""
    from models import storage
    from models.place import Place

    place = storage.get(Place, str(place_id))
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route("/cities/<uuid:city_id>/places", strict_slashes=False,
                 methods=['POST'])
def add_place_account(city_id):
    """Add new place account to the storage"""
    from models import storage
    from models.place import Place
    from models.city import City
    from models.user import User

    city = storage.get(City, str(city_id))
    if not city:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    request_data = request.get_json()
    if "user_id" not in request_data:
        abort(400, "Missing user_id")
    user = storage.get(User, request_data["user_id"])
    if not user:
        abort(404)
    if "name" not in request_data:
        abort(400, "Missing name")
    new_place_account = Place(**request_data)
    new_place_account.save()
    return make_response(jsonify(new_place_account.to_dict()), 201)


@app_views.route("/places/<uuid:place_id>", strict_slashes=False,
                 methods=['PUT'])
def update_place_account(place_id):
    """Update place account info"""
    from models import storage
    from models.place import Place

    place = storage.get(Place, str(place_id))
    if not place:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    request_data = request.get_json()
    for k, v in request_data.items():
        if k == "id" or k == "updated_at" or k == "created_at" or\
                k == "user_id" or k == "city_id":
            continue
        place.__dict__[k] = v
    place.save()
    return jsonify(place.to_dict())


@app_views.route("/places_search", strict_slashes=False, methods=['POST'])
def super_search():
    """To be updated"""
    from models import storage
    from models.place import Place
    from models.state import State
    from models.city import City
    from models.amenity import Amenity

    filtered_places = []
    cities_list = []
    states_list = []
    amenities_list = []
    if not request.is_json:
        abort(400, "Not a JSON")
    if not request.get_json():
        return jsonify([place.to_dict() for place in storage.all(Place)])
    json_states = request.get_json().get("states", None)
    json_cities = request.get_json().get("cities", None)
    json_amenities = request.get_json().get("amenities", None)
    if not json_states and not json_cities and not json_amenities:
        return jsonify([place.to_dict() for place in storage.all(Place)])
    if json_cities:
        for city_id in json_cities:
            city = storage.get(City, city_id)
            if city:
                cities_list.append(city)
    if json_states:
        for state_id in json_states:
            state = storage.get(State, state_id)
            if state:
                states_list.append(state)
    if json_amenities:
        for amenity_id in json_amenities:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                amenities_list.append(amenity)
    for city in cities_list:
        filtered_places += city.places
    for state in states_list:
        cities = state.cities
        for city in cities:
            if city.id not in json_cities:
                filtered_places += city.places
    for amenity in amenities_list:
        for place in filtered_places:
            if amenity.id not in [a.id for a in place.amenities]:
                filtered_places.remove(place)
    return jsonify([place.to_dict() for place in filtered_places])
