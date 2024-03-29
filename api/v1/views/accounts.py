from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from app.models import *
from werkzeug.security import generate_password_hash, check_password_hash


@app_views.route('/accounts', methods=['GET'])
def get_accounts():
    """Get all accounts"""
    accounts = storage.all(Account)
    account_dict = []
    for account in accounts:
        account_dict.append(storage.to_json(account))
    return jsonify(account_dict)

@app_views.route('/accounts/<id>', methods=['GET'])
def get_account_by_id(id: int):
    """Get all accounts by id"""
    account = storage.get(Account, "id", id)
    account_dict = {}
    for acc in account:
        account_dict[acc.id] = storage.to_json(acc)
    return jsonify(account_dict)   

@app_views.route('/accounts/<customer_id>', methods=['POST'])
def create_account_for_customer(customer_id: int):
    """Create an acccount for a customer based on his ID"""
    try:
        r_args = request.get_json()
    except Exception as e:
        r_args = None
    error = None
    if r_args == None:
        error = 'Wrong format. Account_pin Required'
    if error is None:
        pin = r_args.get('pin')
    if error is not None:
        return jsonify({'error': error}) 
    account = Account()
    account.cus_id = customer_id
    account.create_account(pin)
    storage.save(account)
    return jsonify({'success': f"customer, {customer_id}'s account has been created"})


@app_views.route('/accounts', methods=['POST'])
def get_account_by_cus_id():
    """Get all accounts by id"""
    try:
        r_args = request.get_json()
    except Exception as e:
        r_args = None
    error = None
    if r_args == None:
        error = 'Wrong format. The customer id, cus_id is required'
    if error is None:
        cus_id = r_args.get('cus_id')
    if error is not None:
        return jsonify({'error': error}) 
    account = storage.get(Account, "cus_id", int(cus_id))
    account_dict = {}
    for acc in account:
        account_dict[acc.id] = storage.to_json(acc)
    return jsonify(account_dict)   
