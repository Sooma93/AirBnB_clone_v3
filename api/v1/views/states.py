#!/usr/bin/python3
"""states view"""
from flask import Flask
from flask import jsonify, request, abort, make_response
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Gat all states"""
    objects = storage.all(State)
    lista = []
    for state in objects.values():
        lista.append(state.to_dict())
    return jsonify(lista)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Get states"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Delete states"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """CREATE"""
    data_dict = request.get_json(silent=True)
    if not data_dict:
        abort(400, description="Not a JSON")
    if 'name' not in data_dict:
        abort(400, description="Missing name")
    new_state = State(**data_dict)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Put in state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json(silent=True)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
