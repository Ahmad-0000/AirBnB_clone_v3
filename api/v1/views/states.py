#!/usr/bin/python3
"""States blueprint"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/states", strict_slashes=False)
def all_states():
    """Reterive all States from storage"""
    from models import storage
    from models.state import State

    states_dict = storage.all(State)
    states_list = []
    for state in states_dict.values():
        states_list.append(state.to_dict())
    return jsonify(states_list)

@app_views.route("/states/<uuid:state_id>", strict_slashes=False)
def one_state(state_id):
    """Reterive one state from storage"""
    from models import storage
    from models.state import State

    one_state = storage.get(State, str(state_id))
    if one_state:
        return jsonify(one_state.to_dict())
    abort(404)

@app_views.route("/states/<uuid:state_id>", strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """Delete state from the storage"""
    from models import storage
    from models.state import State

    state = storage.get(State, str(state_id))
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})

#@app_views.route("/states", strict_slashes=False, methods=['POST'])
#def add_state():
#    """Add new state in the storage"""
#    from models import storage
#    from models.state import State

#    if not requsest.json:
#        make_response(jsonify())
