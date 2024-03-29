from app import db
from flask_login import UserMixin
from app import login
from werkzeug.security import check_password_hash, generate_password_hash
import random
from datetime import datetime


class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(), index=True, nullable=False, unique=True)
  password_hash = db.Column(db.String(128))
  has_acc = db.Column(db.Integer, default=0, nullable=False)
  def __repr__(self):
    return '<User {}>'.format(self.email)
    
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def associated(self):
    """This returns associated objects in the db"""
    id = self.id
    customer = Customer.query.filter_by(user_id=id).first()
    accounts = Account.query.filter_by(cus_id=customer.id).all()
    return [customer, account]

class Account(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  cus_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
  account_number = db.Column(db.String(100), nullable=False)
  account_pin = db.Column(db.String(4))
  acc_type = db.Column(db.String(240))
  status = db.Column(db.String(10), default='active')
  balance = db.Column(db.Integer)
  bank_name = db.Column(db.String(240), default="Speedy", nullable=False)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)
  req_clos = db.Column(db.String(3), default="No")
  transactions = db.relationship('Transaction', backref='account', lazy='dynamic')

  def create_account_number(self):
    """This function will use the random module to create a unique number"""
    exists = True #bool for if the generated account number exists
    #while exists:
    number = random.randint(1111111111, 9999999999)
    acc_no = Account.query.filter_by(account_number=number).first()
    if acc_no is None:
      exist = False
    self.account_number = number

  def create_account(self, pin):
    """This creates the accoi=unt based on the form's data"""
    self.date_created = datetime.utcnow()
    self.create_account_number()
    self.acc_type = 'savings'
    self.balance = 200000
    self.account_pin = generate_password_hash(str(pin))

  def check_pin(self, pin):
    """Chc=eck to see if a provided pin is correct"""
    return check_password_hash(self.account_pin, str(pin))
  
  def parse_balance(self):
    """Parse the account balance to include comas"""
    balance = list(str(self.balance))
    num = len(str(self.balance))
    j = 0
    if num > 3:
      if num % 3 == 1:
        balance.insert(1, ",")
        for i in range(4, num):
          if i % 3 == 2:
            balance.insert(i+j, ",")
            j+=1
      if num % 3 == 2:
        balance.insert(2, ",")
        for i in range(4, num):
          if i % 3 == 0:
            balance.insert(i+j, ",")
            j+=1
      if num % 3 == 0:
        for i in range(2, num):
          if i % 3 == 0:
            balance.insert(i+j, ",")
            j+=1
    return "".join(balance)
      
class Customer(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
  first_name = db.Column(db.String(140))
  last_name = db.Column(db.String(140))
  email = db.Column(db.String(120), index=True, unique=True)
  phone_number = db.Column(db.String(204), unique=True)
  username = db.Column(db.String(200))
  address = db.relationship('Address', backref='customer', lazy='dynamic')
  dob = db.Column(db.DateTime)
  date_created= db.Column(db.DateTime, default=datetime.utcnow)
  bank_name = db.Column(db.String(240), default="Speedy")
  accounts = db.relationship('Account', backref='customer', lazy='dynamic')

  def __repr__(self):
      return "Customer: {} {}".format(self.first_name, self.last_name)

  @classmethod
  def get(cls, param, arg):
    """Get a customer from the database based on information given"""
    if param == "id":
      customer = Customer.query.filter_by(id=arg).first()
    elif param == "user_id":
      customer = Customer.query.filter_by(user_id=arg).first()
    elif param == "email":
      customer = Customer.query.filter_by(email=arg).first()
    elif param == "phone_number":
      customer == Customer.query.filter_by(phone_number=arg).first()
    else:
      customer = None
    return customer
  
  def format_time(self, date: datetime):
    """This to format object to string"""
    format = ("%B %d %Y")
    return datetime.strftime(date, format)
  
  def date_time(self, date:datetime):
    format = ('%Y-%m-%d')
    return datetime.strftime(date, format)

  def get_address(self):
    """Get customer address"""
    return self.address.first()
  
  def get_accounts(self):
    """Get accounts from the customer"""
    return self.accounts.all()


  def create_customer(self, form, account: Account):
    """This function is to assign values to the attributes of the object"""
    self.first_name = form.firstname.data
    self.last_name = form.lastname.data
    self.dob = form.dob.data
    self.date_created = account.date_created
    self.phone_number = form.phonenumber.data
    self.username = form.username.data



class Transaction(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(250))
  acc_num = db.Column(db.String(100), db.ForeignKey('account.account_number'))
  bank_name = db.Column(db.String(240), default="Speedy", nullable=False)
  transaction_type = db.Column(db.String(240))
  amount = db.Column(db.Integer)
  timestamp = db.Column(db.DateTime)
  initial_balance = db.Column(db.Integer)
  cus_name = db.Column(db.String)
  balance = db.Column(db.Integer)
  ref = db.Column(db.String(256))

  def format_time(self, time):
    """Format time"""
    return datetime.strftime(time, '%m/%d/%Y')
  
  def create_transaction(self, creditor: Account, form, type: str, debitor: Account=None):
    """This creates a transaction object and modifies the account accordingly"""
    self.description = form.description.data
    self.amount = int(form.amount.data)
    self.ref = random.choice(['SPD', 'SPY' 'SPE', 'SPDY']) + "-" + str(random.randint(1111111111, 9999999999)) 
    if type == 'debit':
      if form.description.data == "" or form.description.data == None:
        self.description = 'Online Transfer to a customer' 
      self.initial_balance = creditor.balance
      self.balance = creditor.balance - int(self.amount)
      creditor.balance = self.balance
      self.amount = -1 * self.amount
      self.bank_name = form.bank_name.data
      self.acc_num = debitor.account_number
      customer = Customer.query.filter_by(id=debitor.cus_id).first()
      self.cus_name = customer.first_name + " " + customer.last_name
      self.account = creditor
    else:
      if form.description.data == "" or form.description.data == None:
        self.description = 'Online transfer from a Customer '
      self.initial_balance = debitor.balance
      debitor.balance = debitor.balance + int(self.amount)
      self.balance = debitor.balance
      self.bank_name = creditor.bank_name
      self.acc_num = creditor.account_number
      customer = Customer.query.filter_by(id=creditor.cus_id).first()
      self.cus_name = customer.first_name + " " + customer.last_name
      self.account = debitor
    self.transaction_type = type
    self.timestamp = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

  def parse_balance(self, amount):
    """Parse the account balance to include comas"""
    n_balance = list(str(amount))
    balance = n_balance[:]
    num = len(str(amount))
    if n_balance[0] == "-":
      num -= 1
      balance.pop(0)
    j = 0
    if num > 3:
      if num % 3 == 1:
        balance.insert(1, ",")
        for i in range(4, num):
          if i % 3 == 2:
            balance.insert(i+j, ",")
            j+=1
      if num % 3 == 2:
        balance.insert(2, ",")
        for i in range(4, num):
          if i % 3 == 0:
            balance.insert(i+j, ",")
            j+=1
      if num % 3 == 0:
        for i in range(2, num):
          if i % 3 == 0:
            balance.insert(i+j, ",")
            j+=1
    if n_balance[0] == "-":
      balance.insert(0, "-")
    return "".join(balance)
      

  @classmethod
  def get_dated_transaction(cls, start: datetime, end: datetime, transactions):
    """Get the transactions in a time interval"""
    transactions_list = []
    for transaction in transactions:
      if transaction.timestamp >= start and transaction.timestamp <= end:
        transactions_list.append(transaction)
      if transaction.timestamp > end:
        break
    return transactions_list
  
  
class Transact(db.Model):
  """A class on the transaction type"""
  id = db.Column(db.Integer, primary_key=True)
  transaction_id_creditor = db.Column(db.Integer, db.ForeignKey('transaction.id'))
  transaction_id_debitor = db.Column(db.Integer, db.ForeignKey('transaction.id'))
  crebitor = db.Column(db.Integer, db.ForeignKey('account.account_number'))
  deditor =  db.Column(db.Integer, db.ForeignKey('account.account_number'))

  def transact(self, creditor:Account, debitor:Account, form):
    """Create transaction records"""
    transaction_creditor = Transaction()
    transaction_debitor = Transaction()
    self.creditor = creditor.account_number
    self.deditor = debitor.account_number
    self.transaction_id_creditor = transaction_creditor.id
    self.transaction_id_debitor = transaction_debitor.id
    transaction_creditor.create_transaction(creditor, form, "debit", debitor)
    transaction_debitor.create_transaction(creditor, form, "credit", debitor)
    db.session.add(transaction_creditor)
    db.session.add(transaction_debitor)

  
class Address(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  cus_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
  apartment_number = db.Column(db.Integer, nullable=False)
  street_number = db.Column(db.Integer)
  street_name = db.Column(db.String(256), nullable=False)
  city = db.Column(db.String(256), nullable=False)
  state = db.Column(db.String(256), nullable=False)
  country = db.Column(db.String(256), nullable=False)
  postal_code = db.Column(db.Integer)
  address_line_2 = db.Column(db.String(400))

  def create_address(self, form):
    """Fill in the address attribute """
    self.apartment_number = form.apartment_number.data
    self.street_name = form.street_name.data
    self.city = form.city.data
    self.state = form.state.data
    self.country = form.country.data
    self.postal_code = form.postal_code.data
    self.address_line_2 = form.address_line_2.data

class ClosedAccounts(db.Model):
  """This class creates object for closed fintech accounts """
  id = db.Column(db.Integer, primary_key=True)
  acc_num = db.Column(db.String(15), nullable=False)
  acc_pin = db.Column(db.String(4), nullable=False)
  cus_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
  user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
  acc_balance = db.Column(db.Integer)
  date_closed = db.Column(db.DateTime)
  acc_type = db.Column(db.String(240))
  bank_name = db.Column(db.String(240), default="Speedy", nullable=False)
  close_reason = db.Column(db.String(256))
  date_acc_created = db.Column(db.DateTime)
  

  def close_account(self, acc: Account):
    """This is the function to call to close the account"""
    self.acc_num = acc.account_number
    self.acc_pin = acc.account_pin
    self.cus_id = acc.cus_id
    self.timestamp = datetime.utcnow().replace(hour=0, minute=0, microsecond=0)
    self.acc_balance = acc.balance
    self.date_acc_created = acc.date_created
    self.acc_type = acc.acc_type
    self.bank_name = acc.bank_name

class DeletedAccount(db.Model):
  """Class for deleted accounts"""
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer)
  customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))


@login.user_loader
def load_user(id):
  return User.query.get(int(id))