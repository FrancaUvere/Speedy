#!/usr/bin/env python3
"""Error handling"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from app.models import *


@app_views.errorhandler(404)
def not_found():
    """Deal with the not-found error"""
    return jsonify("{'error': 'info not found'}")

@app_views.errorhandler(405)
def wrong_method():
    """Deal with not allowed methds"""
    return jsonify({'error': 'Method not allowed'})