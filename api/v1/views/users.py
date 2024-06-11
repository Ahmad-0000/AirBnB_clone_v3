#!/usr/bin/python3
"""User blueprint"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/users", strict_slashes=False)
def all_users():
    """Reterive all user accounts from storage"""
    from models import storage
    from models.user import User

    users_dict = storage.all(User)
    users_list = []
    for user in users_dict.values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route("/users/<uuid:user_id>", strict_slashes=False)
def one_user(user_id):
    """Reterive one user account from storage"""
    from models import storage
    from models.user import User

    user = storage.get(User, str(user_id))
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<uuid:user_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_user_account(user_id):
    """Delete one user account from storage"""
    from models import storage
    from models.user import User

    user = storage.get(User, str(user_id))
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route("/users", strict_slashes=False, methods=['POST'])
def add_user_account():
    """Add new user account to the storage"""
    from models.user import User

    if not request.is_json:
        abort(400, "Not a JSON")
    request_data = request.get_json()
    if "email" not in request_data:
        abort(400, "Missing email")
    if "password" not in request_data:
        abort(400, "Missing password")
    new_user_account = User(**request_data)
    new_user_account.save()
    return make_response(jsonify(new_user_account.to_dict()), 201)


@app_views.route("/users/<uuid:user_id>", strict_slashes=False,
                 methods=['PUT'])
def update_user_account(user_id):
    """Update user account info info"""
    from models import storage
    from models.user import User

    user = storage.get(User, str(user_id))
    if not user:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    request_data = request.get_json()
    for k, v in request_data.items():
        if k == "id" or k == "updated_at" or k == "created_at" or k == "email":
            continue
        user.__dict__[k] = v
    user.save()
    return jsonify(user.to_dict())
