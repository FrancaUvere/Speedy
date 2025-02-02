from app import app
from app.models import User, Account, Transaction, Customer, Address
from app import db


@app.shell_context_processor
def make_shell_context():
  return {'db': db, 'User': User, 'Transaction': Transaction, 'Customer': Customer, 'Account': Account, 'Address': Address}

if __name__ == '__main__':
  app.run(port=5050, debug=True)