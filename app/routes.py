from flask import Flask, redirect, render_template, request, url_for, flash, Response
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.forms import *
from app import app, db
from app.models import *
from datetime import datetime
import random
from weasyprint import HTML, CSS



@app.route('/', methods=['GET'])
def home():    
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.has_acc == 1:
        customer: Customer = Customer.query.filter_by(user_id=current_user.id).first()
        if customer.address.first() == None:
            return redirect(url_for('add_address', username=customer.username))
        return redirect(url_for('user_home', username=customer.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        if current_user.has_acc == 0:
            return redirect(url_for('create_account'))
        customer: Customer = Customer.query.filter_by(user_id=current_user.id).first()
        if customer.address.first() == None:
            return redirect(url_for('add_address', username=customer.username))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user_home', username=customer.username)
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated and current_user.has_acc == 1:
        customer: Customer = Customer.query.filter_by(user_id=current_user.id).first()
        if customer.address.first() == None:
            return redirect(url_for('add_address', username=customer.username))
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    if hasattr(current_user, 'has_acc') and current_user.has_acc == 1:
        customer: Customer = Customer.query.filter_by(user_id=current_user.id).first()
        if customer.address.first() == None:
            return redirect(url_for('add_address', username=customer.username))
        return redirect('home')
    form = CreateAccountForm()
    if form.validate_on_submit():
        flash('Account successfully created')
        current_user.has_acc = 1
        customer =Customer()
        account = Account()
        account.create_account(form.pin.data)
        account.customer = customer
        customer.create_customer(form, account)
        customer.email = current_user.email
        customer.user_id = current_user.id
        account.cus_id = customer.id
        db.session.add(customer)
        db.session.commit()
        db.session.add(account)
        db.session.commit()
        return redirect(url_for('add_address', username=customer.username))
    return render_template('acc_creation.html', form=form)


@app.route('/<username>/create-account', methods=['GET', 'POST'])
@login_required
def create_acc(username):
    customer: Customer = Customer.get('user_id', current_user.id)
    form = CreateUserAccountForm()
    if form.validate_on_submit():
        new_account = Account()
        new_account.create_account(form.pin.data)
        new_account.customer = customer
        db.session.add(new_account)
        db.session.commit()
        flash(f'Account {new_account.account_number} successfully created', 'success')
        return redirect(url_for('accounts', username=customer.username))
    return render_template('create_user_account.html', form=form, customer=customer)


@app.route('/<username>/add-address', methods=['GET', 'POST'])
@login_required
def add_address(username):
    customer: Customer = Customer.query.filter_by(user_id=current_user.id).first()
    if username != customer.username:
        return redirect(url_for('user_home', username=customer.username))
    form = FillAddress()
    if form.validate_on_submit():
        flash('Address Successfully added')
        customer = Customer.query.filter_by(user_id=current_user.id).first()
        address: Address = Address()
        address.cus_id = customer.id
        address.create_address(form)
        db.session.add(address)
        db.session.commit()
        return redirect(url_for('user_home', username=username))
    return render_template('set_address.html', form=form)

@app.route('/<username>/home')
@login_required
def user_home(username):
    customer: Customer = Customer.query.filter_by(user_id=current_user.id).first()
    accounts = Account.query.filter_by(cus_id=customer.id).all()
    for account in accounts:
            if account.req_clos == 'Yes':
                accounts.remove(account)
    if username != customer.username:
        return redirect(url_for('user_home', username=customer.username))
    return render_template('user_home.html', username=username, customer=customer, account=accounts[0])

@app.route('/<username>/profile', methods=['GET'])
@login_required
def profile(username):
    """Profile page for user"""
    customer: Customer = Customer.query.filter_by(user_id=current_user.id).first()
    accounts=Account.query.filter_by(cus_id=customer.id)
    if username != customer.username:
        return redirect(url_for('user_home', username=customer.username))
    return render_template('user_profile.html', username=customer.username, customer=customer)

@app.route('/<username>/profile/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    """Edit the profile of the user"""
    customer: Customer = Customer.query.filter_by(user_id=current_user.id).first()
    if username != customer.username:
        return redirect(url_for('user_home', username=customer.username))
    form = EditProfileInfo()
    form2=EditProfileAddress()
    if form.validate_on_submit():
        customer.phone_number = form.phonenumber.data
        customer.username = form.username.data
        db.session.commit()
        return redirect(url_for('edit_profile', username=customer.username))
    if form2.validate_on_submit():
        address = Address.query.filter_by(cus_id=customer.id).first()
        address.create_address(form2)
        db.session.commit()
        return redirect(url_for('edit_profile', username=customer.username))
    return render_template('edit_profile.html', username=customer.username, customer=customer, form=form, form2=form2)

@app.route('/<username>/transactions', methods=['GET', 'POST'])
@login_required
def transactions(username):
    """Route function for the transactions page"""
    customer: Customer = Customer.query.filter_by(user_id=current_user.id).first()
    if username != customer.username:
        return redirect(url_for('user-home', username=customer.username))
    cus = Customer.query.filter_by(username=username).first()
    accounts = cus.accounts.all()
    for account in accounts:
            if account.req_clos == 'Yes':
                accounts.remove(account)
    transactions = accounts[0].transactions
    transactions = list(transactions)
    transactions.reverse()
    form = GenerateStatement()
    if form.validate_on_submit():
        id = request.args.get('id')
        account: Account = Account.query.filter_by(id=id).first()
        transactions = account.transactions.all()
        start = datetime(form.start.data.year, form.start.data.month, form.start.data.day)
        end = datetime(form.end.data.year, form.end.data.month, form.end.data.day)
        transact_list = Transaction.get_dated_transaction(start, end, transactions)
        customer = Customer.query.filter_by(user_id=current_user.id).first()
        rendered = render_template('e_statement.html', username=customer.username, customer=customer, account=account, transactions=transact_list)
        htm_render = render_template('transactions.html', transactions=transactions, accounts=accounts, customer=customer, username=customer.username, form=form)
        with open('app/static/styles/e_statement.css', 'rb') as css_file:
            css_content = css_file.read()
        pdf = HTML(string=rendered).write_pdf(stylesheets=[CSS(string=css_content)])
        # Create a Flask Response object with the PDF content
        response = Response(pdf, content_type='application/pdf')
        response.headers['Content-Disposition'] = f'attachment; filename="{customer.first_name} {customer.last_name} statement_pdf.pdf"'
        return response
    if 'id' not in request.args:
        return redirect(url_for('transactions', id=accounts[0].id, username=customer.username))
    if 'id' in request.args:
        id = request.args.get('id')
        accounts = cus.accounts.all()
        for account in accounts:
            if account.req_clos == 'Yes':
                accounts.remove(account)
        account  = Account.query.filter_by(id=id).first()
        accounts.remove(account)
        accounts.insert(0, account)
        transactions = account.transactions
        transactions = list(transactions)
        transactions.reverse()
        return render_template('transactions.html', transactions=transactions, accounts=accounts, customer=customer, username=customer.username, form=form)
    return render_template('transactions.html', transactions=transactions, accounts=accounts, customer=customer, username=customer.username, form=form)


@app.route('/<username>/transfer', methods=['GET', 'POST'])
@login_required
def transfer(username):
    """Route function for making transfers"""
    customer: Customer = Customer.query.filter_by(user_id=current_user.id).first()
    if username != customer.username:
        return redirect(url_for('user_home', username=customer.username))
    user = User.query.all()
    form = Transfer()
    accounts = customer.accounts.all()
    for account in accounts:
        if account.req_clos == 'Yes':
            accounts.remove(account)
    if 'id' in request.args:
        account: Account = Account.query.filter_by(id=request.args.get('id')).first()
        accounts.remove(account)
        accounts.insert(0, account)
    if 'id' not in request.args:
        return redirect(url_for('transfer', id=accounts[0].id, username=customer.username))
    if form.validate_on_submit():
        creditor = Account.query.filter_by(id=request.args.get('id')).first()
        debitor = Account.query.filter_by(account_number=form.acc_number.data).first()
        transact = Transact()
        transact.transact(creditor, debitor, form)
        db.session.add(transact)
        db.session.commit()
        return redirect(url_for('transactions', username=customer.username, id=request.args.get('id')))
    return render_template('make_transfer.html', username=customer.username, form=form, customer=customer, users=user, accounts=accounts)




@app.route('/<username>/accounts')
@login_required
def accounts(username):
    customer: Customer = Customer.query.filter_by(user_id=current_user.id).first()
    if username != customer.username:
        return redirect(url_for('user_home', username=customer.username))
    accounts = customer.accounts
    return render_template('accounts.html', customer=customer, accounts=accounts)

@app.route('/<username>/accounts/<id>')
@login_required
def account(username, id):
    customer: Customer = Customer.get('user_id', current_user.id)
    if username != customer.username:
        return redirect(url_for('user_home', username=customer.username))
    account = Account.query.filter_by(id=id).first()
    transactions = account.transactions
    transactions = list(transactions)
    transactions.reverse()
    return render_template('account.html', customer=customer, account=account, transactions=transactions, id=id)


@app.route('/<username>/services')
@login_required
def services(username):
    customer: Customer = Customer.query.filter_by(user_id=current_user.id).first()
    if username != customer.username:
        return redirect(url_for('user_home', username=customer.username))
    customer = Customer.get('user_id', current_user.id)
    return render_template('services.html', customer=customer)

@app.route('/<username>/profile/manage_accounts', methods=['POST', 'GET'])
@login_required
def manage_accounts(username):
    """Manage all accounts"""
    customer: Customer = Customer.query.filter_by(user_id=current_user.id).first()
    if username != customer.username:
        return redirect(url_for('user_home', username=customer.username))
    accounts = customer.accounts
    for account in accounts:
            if account.req_clos == 'Yes':
                accounts.remove(account)
    form = VerifyPin()
    if form.is_submitted():
        if form.validate():
            return redirect(url_for('new_password', username=customer.username, id=request.args.get('id')))
        else:
            flash('Wrong Pin')
    return render_template('manage_account.html', username=customer.username, accounts=accounts, customer=customer, form=form)

@app.route('/<username>/profile/manage_accounts/new_pin', methods=['POST', 'GET'])
def new_password(username):
    """The new password function route"""
    customer: Customer = Customer.query.filter_by(user_id=current_user.id).first()
    if username != customer.username:
        return redirect(url_for('user_home', username=customer.username))
    accounts = customer.accounts
    for account in accounts:
            if account.req_clos == 'Yes':
                accounts.remove(account)
    form = VerifyPin()
    form2 = NewPin() 
    if form2.validate_on_submit():
        flash('New Password Successfully Changed')
        id = request.args.get('id')
        account = Account.query.filter_by(id=id).first()
        account.account_pin = generate_password_hash(str(form2.pin.data))
        db.session.commit()
        return redirect(url_for('manage_accounts', username=customer.username))
    return render_template('manage_account.html', username=customer.username, accounts=accounts, customer=customer, form=form, form2=form2)

@app.route('/<username>/profile/manage_accounts/close_account', methods=['POST', 'GET'])
@login_required
def close_account(username):
    """Route for close account"""
    customer: Customer = Customer.query.filter_by(user_id=current_user.id).first()
    if username != customer.username:
        return redirect(url_for('user_home', username=customer.username))
    accounts = customer.accounts
    for account in accounts:
            if account.req_clos == 'Yes':
                accounts.remove(account)
    form3 = CloseAccount()
    if form3.validate_on_submit():
        account: Account = Account.query.filter_by(account_number=form3.acc_num.data).first()
        if account.req_clos == 'Yes':
            flash('Account already requested for closure or closed')
        else:
            account.req_clos = 'Yes'
            db.session.commit()
            closed_account = ClosedAccounts()
            closed_account.user_id = current_user.id
            if form3.reason.data:
                closed_account.close_reason = form3.reason.data
            closed_account.close_account(account)
            db.session.add(closed_account)
            db.session.commit()
            flash('Closure request succesfully sent')
        return redirect(url_for('manage_accounts', username=customer.username))
    return render_template('manage_account.html', username=customer.username, accounts=accounts, customer=customer, form3=form3)

@app.route('/<username>/profile/manage_user_account', methods=['GET', 'POST'])
def user_acc(username):
    """Edit the user account details"""
    customer: Customer = Customer.query.filter_by(user_id=current_user.id).first()
    if username != customer.username:
        return redirect(url_for('user_home', username=customer.username))
    form1 = ChangeEmail()
    if form1.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        user.email = form1.email.data
        customer.email = form1.email.data
        current_user.email = form1.email.data
        db.session.commit()
        return render_template('manage_user_account.html', username=customer.username, customer=customer, form1=form1)
    return render_template('manage_user_account.html', username=customer.username, customer=customer, form1=form1)

@app.route('/<username>/profile/manage_user_account/change_password', methods=['GET', 'POST'])
def change_password(username):
    """Change user password"""
    customer: Customer = Customer.query.filter_by(user_id=current_user.id).first()
    if username != customer.username:
        return redirect(url_for('user_home', username=customer.username))
    form1 = ChangeEmail()
    form2 = ChangePassword()
    if form2.validate_on_submit():
        current_user.password_hash = generate_password_hash(form2.new_password.data)
        db.session.commit()
        return render_template('manage_user_account.html', username=customer.username, customer=customer, form1=form1)
    return render_template('manage_user_account.html', username=customer.username, customer=customer, form1=form1, form2=form2)

@app.route('/<username>/profile/manage_user_account/delete_account', methods=['GET', 'POST'])
def delete_account(username):
    """Delete user account"""
    customer: Customer = Customer.query.filter_by(user_id=current_user.id).first()
    if username != customer.username:
        return redirect(url_for('user_home', username=customer.username))
    form1 = ChangeEmail()
    form3 = DeleteAccount()
    if form3.validate_on_submit():
        deleted_account = DeletedAccount()
        deleted_account.user_id = current_user.id
        deleted_account.customer_id = customer.id
        user = User.query.filter_by(id=current_user.id).first()
        db.session.add(deleted_account)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('logout'))
    return render_template('manage_user_account.html', username=customer.username, customer=customer, form1=form1, form3=form3)

@app.route('/<username>/contact')
def contact(username):
    customer: Customer = Customer.get('user_id', current_user.id)
    return render_template('contact.html', customer=customer)
   
    
@app.route('/contact_us', methods=['GET', 'POST'])
def land_contact():
    form = ContactUs()
    if form.validate_on_submit():
        return render_template('land_contact.html', form=form)
    return render_template('land_contact.html', form=form)





@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

