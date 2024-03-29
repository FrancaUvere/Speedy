#!/usr/bin/env python3
"""Routes to get users"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from app.models import *
from werkzeug.security import generate_password_hash, check_password_hash

@app_views.route('/users', methods=['GET'])
def get_users():
    users = storage.all(User)
    user_dict = {}
    user_list = []
    for user in users:
        user_list.append(storage.to_json(user))
    user_dict['user'] = user_list
    return jsonify(user_dict)


#methods on user/user_id

@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id: int = None) ->str:
    """This is to get the user id by name"""
    if user_id is None:
            return {}
    user = storage.get(User, "id", user_id )
    if user is None:
         return jsonify({'error': f'user {user_id} not found'})
    
    return jsonify(storage.to_json(user))
  
         

@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id: int=None):
    if user_id is None:
        return {}
    user = storage.get(User, "id", user_id )
    if user is None:
        return jsonify({'Deletion failed': f"Cannot delete user {user_id}. User doesn't exist"})
    storage.delete(user)
    return jsonify({'success': f'user {user_id} deleted from database'})
    
@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id: int=None):
    """Update a user information"""
    if user_id is None:
        return {}
    user = storage.get(User, "id", user_id )
    if user is None:
        return jsonify({'Update failed': f"Cannot update user {user_id}. User doesn't exist"})
    try:
        request_args = request.get_json()
    except Exception as e:
        request_args = None
    error = None
    if request_args is None:
        error = "Wrong format"
    if error is not None and request_args.get('email') is None and request_args.get('has_acc') is None:
        error = 'No email or has_acc status specified'
    if len(request_args.keys()) > 2:
        error = "Only email and has_acc can be updated"
    if error is None:
        try:
            if request_args.get('email') is not None:
                user.email = request_args.get('email')
            if request_args.get('has_acc') is not None:
                user.has_acc = int(request_args.get('has_acc'))
        except Exception as e:
            error ="Cannot update user"
    if error is not None:
        return jsonify({'error': error})
    storage.save()
    return jsonify({'success': f"user {user_id} successfuly updated"})
        
    
@app_views.route('/users', methods=['POST'])
def create_user():
    """Create user """
    try:
        r_args = request.get_json()
    except Exception as e:
        r_args = None
    error = None
    if r_args == None:
        error = 'Wrong format. Email Required'
    if error is None:
        email = r_args.get('email')
        password = r_args.get('password')
        if email is None:
            error = 'Email required'
        if error is None and password is None:
            error = 'Password required'
        if error is None and len(r_args.keys()) > 2:
            error = 'Only email and password is needed for the creation of a user'
    if error is not None:
        return jsonify({'error': error}) 
    user = User()
    user.email = email
    user.password_hash = generate_password_hash(password)
    storage.save(user)
    return jsonify({'success': f"user, {user.id} has been created"})     
