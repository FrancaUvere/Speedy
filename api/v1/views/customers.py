from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from app.models import *
from werkzeug.security import generate_password_hash, check_password_hash

@app_views.route('/customers', methods=['GET'])
def get_customers():
    """Get all customer in the database"""
    customers = storage.all(Customer)
    customers_dict = {}
    attr_list = []
    for customer in customers:
        attr_list.append(storage.to_json(customer))
    customers_dict['Customers'] = attr_list
    return jsonify(customers_dict)

@app_views.route('/customers/<customer_id>', methods=['GET'])
def get_customer_id(customer_id: int):
    try:
        int(customer_id)
    except Exception as e:
        return jsonify({'error': f"{customer_id} is not an integer"})
    customer = Customer.get("id", customer_id)
    if customer is None:
        return jsonify({'error': f"customer with id {customer_id} not found"})
    customer_dict = storage.to_json(customer)
    return jsonify(customer_dict)

@app_views.route('/customers/find', methods=['POST'])
def get_customer_find():
    """Get customer by a specidfies parameter"""
    rj_args = request.args
    error = None
    if rj_args is None:
        error = 'specify arguments: email or phone_number'
    if rj_args is not None:
        if len(rj_args) > 1:
            error = 'specify only one argument, email or phone_number'
        if list(rj_args.keys())[0] not in ['email', 'phone_number']:
            error = 'Specify one of this argument, email or phone_number'
    if error is None:
        param = list(rj_args.keys())[0]
        arg = list(rj_args.items())[0]
        customer = Customer.get(param, arg)
        if customer is None:
            error = 'Customer not found'
        if customer is not None:
            return jsonify(storage.to_json(customer))
    return jsonify({'error': error})
