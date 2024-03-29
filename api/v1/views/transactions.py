#!/usr/bin/python3
"""Transactions api"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from app.models import *
from werkzeug.security import generate_password_hash, check_password_hash


@app_views.route('/transactions')
def get_transactions():
    """Get all transactions"""
    transactions = storage.all(Transaction)
    transaction_dict = {}
    for transaction in transactions:
        transaction_dict[transaction.id] = storage.to_json(transaction)
    return jsonify(transaction_dict)