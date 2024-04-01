#!/usr/bin/python3
"""Handles all default RESTful API actions for State objects."""

from flask import jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views

# Retrieves the list of all State objects
@app_views.route('/states', methods=['GET'])
def get_states():
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])

# Retrieves a State object by state_id
@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())

# Deletes a State object by state_id
@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

# Creates a new State
@app_views.route('/states', methods=['POST'])
def create_state():
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    data = request.get_json()
    state = State(**data)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201

# Updates a State object by state_id
@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
