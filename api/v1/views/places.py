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
    storage.close()
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
    storage.close()
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
    storage.close()
    return jsonify(place.to_dict())
