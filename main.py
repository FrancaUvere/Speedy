#!/usr/bin/env python3
"""Populating the database"""

from app import db
from app.models import *
import json
import requests
import random
from werkzeug.security import generate_password_hash, check_password_hash
import asyncio
from datetime import datetime

# account: Account = Account.query.filter_by(id=16).first()
# # account.req_clos = 'Yes'
# # db.session.commit()
# print(account.req_clos)
# account.account_pin = generate_password_hash(str(1234))
# db.session.commit()

