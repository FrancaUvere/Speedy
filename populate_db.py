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

new_user_info = {}
bank_name = ['Speedy', 'Dainty Bank']
address_dict = [{"apartment_number":528,"street_number":6801,"street_name":"Scofield","city":"Klonowa","postal_code":"98-273","country":"Poland","address_line_2":"Room 1467", "state":"Klonowa"},
{"apartment_number":519,"street_number":9743,"street_name":"Myrtle","city":"Bykhaw","country":"Belarus","address_line_2":"16th Floor", "state": "Mogilev"},
{"apartment_number":906,"street_number":2299,"street_name":"Washington","city":"Virje","postal_code":"48326","country":"Croatia","address_line_2":"PO Box 10151", "state": "Koprivincia"},
{"apartment_number":373,"street_number":9605,"street_name":"Northwestern","city":"Asamboka","country":"Indonesia","address_line_2":"16th Floor", "state": "Unknown"},
{"apartment_number":622,"street_number":2566,"street_name":"7th","city":"Xaçmaz","country":"Azerbaijan","address_line_2":"17th Floor", "state": "Unkown"},
{"apartment_number":656,"street_number":8496,"street_name":"Burrows","city":"Sagae","postal_code":"991-0041","country":"Japan","address_line_2":"Suite 22", "state": "Unknown"},
{"apartment_number":921,"street_number":9761,"street_name":"Sommers","city":"Silva Jardim","postal_code":"28820-000","country":"Brazil","address_line_2":"6th Floor", "state": "Unknown"},
{"apartment_number":938,"street_number":3773,"street_name":"Weeping Birch","city":"Dongyang","country":"China","address_line_2":"9th Floor", "state": "Unknown"},
{"apartment_number":243,"street_number":3444,"street_name":"Reinke","city":"El Alto","country":"Peru","address_line_2":"PO Box 20327", "state": "Unkown"},
{"apartment_number":721,"street_number":4537,"street_name":"Holmberg","city":"Kunyang","country":"China","address_line_2":"Apt 754", "state": "unknown"}]
dob = [{"date of birth":"6/7/1978"},
{"date of birth":"10/9/1925"},
{"date of birth":"5/24/1945"},
{"date of birth":"8/24/1906"},
{"date of birth":"6/7/1930"},
{"date of birth":"4/11/1924"},
{"date of birth":"1/7/1991"},
{"date of birth":"12/12/1905"},
{"date of birth":"3/21/1921"},
{"date of birth":"10/3/1996"}]
phone_number = [{"phone_number":"813-600-4396"},
{"phone_number":"314-719-8011"},
{"phone_number":"405-438-0126"},
{"phone_number":"232-279-9841"},
{"phone_number":"594-862-4637"},
{"phone_number":"875-829-4752"},
{"phone_number":"430-866-1763"},
{"phone_number":"294-378-7587"},
{"phone_number":"863-835-4891"},
{"phone_number":"714-630-9834"}]
account_nos = [{"account_number":"4812659639"},
{"account_number":"7207068948"},
{"account_number":"1717488595"},
{"account_number":"2509854836"},
{"account_number":"5711617532"},
{"account_number":"1367169747"},
{"account_number":"3693415390"},
{"account_number":"2809267634"},
{"account_number":"7253194748"},
{"account_number":"9852917978"}]
password_bank = 'password.json'
new_user = 'user.json'
new_customer = 'customer.json'
new_account = 'accounts.json'
password_info = {}
date_format = '%m/%d/%Y'


def account_populate(obj: Account, dict: dict, bank):
    obj.cus_id = dict['id']
    obj.acc_type = dict['account_type']
    obj.balance = dict['balance']
    obj.date_created = dict['date_opened']
    obj.bank_name = bank


def address_populate(obj: Address, dict: dict):
    for k, v in dict.items():
        if hasattr(obj, k):
            if k == 'id':
                continue
            setattr(obj, k, v)

def populate_database():
    with open('models/engine/user_details.json', 'r') as f:
        objs = json.loads(f.readline())
        j = 0
        for obj in objs:
            if j < 10:
                user = User()
                account = Account()
                customer = Customer()
                address = Address()
                word_one = requests.get("https://random-word-api.herokuapp.com/word").json()[0]
                word_two = requests.get("https://random-word-api.herokuapp.com/word").json()[0]
                password = word_one + word_two
                if len(password) > 6:
                    password = password[0:random.randint(5, len(password))]
                for k, v in obj.items():
                    if hasattr(user, k):
                        setattr(user, k, v)
                    if hasattr(customer, k):
                        if k == 'id':
                            customer.user_id = user.id
                            customer.id = v
                            continue
                        setattr(customer, k, v)
                    customer.date_created = datetime.strptime(obj['date_opened'], date_format)
                print(j)
                customer.dob = dob[j]['date of birth']
                customer.phone_number = phone_number[j]['phone_number']
                customer.bank_name = random.choice(bank_name)
                password_hash = generate_password_hash(password)
                password_info[user.email] = password
                user.password_hash = password_hash
                account_populate(account, obj, customer.bank_name)
                account.account_number = account_nos[j]['account_number']
                address_populate(address, address_dict[j])
                address.cus_id = customer.id
                customer.dob = datetime.strptime(customer.dob, date_format)
                account.date_created = datetime.strptime(account.date_created, date_format)
                db.session.add(user)
                db.session.commit()
                db.session.add(account)
                db.session.commit()
                db.session.add(customer)
                db.session.commit()
                db.session.add(address)
                db.session.commit()
                j+=1
       
    
populate_database()
with open('password.json', 'w') as f:
    json.dump(password_info, f)

users = User.query.all()
user = User.query.filter_by(id=1).first()
account = Account.query.filter_by(id=1).first()
customer = Customer.query.filter_by(id=1).first()
address = Address.query.filter_by(id=1).first()
print(len(users))
print(user.__dict__)
print(account.__dict__)
print(customer.__dict__)
print(address.__dict__)
             

pins = {}
account = Account.query.all()
for accoun in account:
    pin = str(random.randint(1111, 9999))
    accoun.account_pin = generate_password_hash(pin)
    pins[accoun.id] = pin
    db.session.commit()

with open('accounts.json', 'w') as f:
    json.dump(pins, f)



        


