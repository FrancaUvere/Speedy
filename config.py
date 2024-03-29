#!/usr/bin/env python3
"""Config script in python"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Config class for flask app"""

    SECRET_KEY = os.getenv('SECRET_KEY') or 'lets-make-it-something'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False