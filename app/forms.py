from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField, TextAreaField, PasswordField
from wtforms.validators import Regexp, Length
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask import request
from flask_login import current_user
from werkzeug.security import check_password_hash

class LoginForm(FlaskForm):
    """
    This class represents the login web form
    It gets inputs from the user using wtforms fields.
    (StringField, PasswordField, SubmitField)
    """
    email = StringField('Email address', validators=[DataRequired(), Length(min=7, max=40), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """
    This class represents the Sign up web form
    It gets inputs from the user using wtforms fields.
    (StringField, PasswordField, SubmitField)
    """
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class CreateAccountForm(FlaskForm):
    """Create an account form"""
    firstname = StringField('First name', validators=[DataRequired()])
    lastname = StringField('Last name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    phonenumber = StringField('Phone number', validators=[DataRequired()])
    dob = DateField('Date of Birth:', validators=[DataRequired()], format='%Y-%m-%d')
    pin = PasswordField('Set Pin', validators=[DataRequired(), Length(min=4, max=4, message="Pin must be 4 digits")])
    email = StringField('Email')
    create = SubmitField('Create account')
    

    def validate_firstname(self, firstname):
        integer = 0
        try: 
            int(firstname)
            integer = 1
        except Exception:
            pass
        if integer == 1:
            ValidationError('Firstname must not be a number')
    
    def validate_lastname(self, lastname):
        integer = 0
        try: 
            int(lastname)
            integer = 1
        except Exception:
            pass
        if integer == 1:
            raise ValidationError('Lastname must not be a number')

    def validate_phonenumber(self, phonenumber):
        """validate the phonenmber"""
        from app.models import Customer
        phone_no = phonenumber.data
        customer = Customer.query.filter_by(phone_number=phone_no).first()
        if customer is not None:
            raise ValidationError('Phonenumber already in use')
        if phonenumber.data[0] == 0:
            phone_no = phonenumber.data[1:]
        try:
            int(phone_no)
        except Exception:
            raise ValidationError('Phonenumber cannot be words')
    
    def validate_pin(self, pin):
        try:
            int(pin.data)
        except Exception:
            raise ValidationError('The pin should be digits')
        
    def validate_username(self, username):
        """Validate username"""
        from app.models import Customer
        customer = Customer.query.filter_by(username=username.data).first()
        if customer is not None:
            raise ValidationError('Username already taken.')


class CreateUserAccountForm(FlaskForm):
    email = StringField('Email')
    phonenumber = StringField('Phone number')
    dob = DateField('Date of Birth:', format='%Y-%m-%d')
    pin = PasswordField('Set Pin', validators=[DataRequired(), Length(min=4, max=4, message="Pin must be 4 digits")])
    create = SubmitField('Create account')


class FillAddress(FlaskForm):
    """This is a class of form to fill address"""
    apartment_number = StringField('Apartment number', validators=[DataRequired(), Regexp(regex=r'\d*', message='Values must be digits')])
    street_name = StringField('Street name', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    postal_code = StringField('Postal Code', validators=[Regexp(regex=r'\d*', message='Values must be digits')])
    address_line_2 = StringField('Address Line 2')
    submit = SubmitField('Add address')


class Transfer(FlaskForm):
    """Form to carry out transfers"""
    amount = StringField('Amount', validators=[DataRequired()])
    acc_number = StringField('Beneficiary Account Number', validators=[DataRequired(),  Length(min=9, max=10, message="Account number must be 10 digits only")])
    bank_name = SelectField('Beneficiary Bank Name', choices=[('Speedy', 'Speedy'), ('Dainty Bank', 'Dainty Bank')], validators=[DataRequired()])
    description = TextAreaField('Transfer Description', validators=[Length(max=250)])
    pin = PasswordField('Account Pin', validators=[DataRequired(), Length(min=4, max=4)])
    submit = SubmitField('Transfer')

    def validate_amount(self, amount):
        """Validate the amount"""
        from app.models import Account
        if int(amount.data) < 50:
            raise ValidationError('The minimum amount for transfer is 50 naira')
        id = request.args.get('id')
        account = Account.query.filter_by(id=id).first()
        if int(amount.data) > account.balance:
            raise ValidationError('This amount is greater than your account balance')

    def validate_acc_number(self, acc_number):
        """Check if the account number exists for the selected bank"""
        from app.models import Account
        account = Account.query.filter_by(account_number=acc_number.data).first()
        if account is None or account.bank_name != self.bank_name.data:
            raise ValidationError("Error with the account number or bank selected")
    
    def validate_pin(self, pin):
        """Validate the validity of the pin"""
        from app.models import Account
        id = request.args.get('id')
        account = Account.query.filter_by(id=id).first()
        try:
            int(account.account_pin)
            if pin.data != account.account_pin:
                raise ValidationError('Wrong pins')
        except Exception:
            if check_password_hash(account.account_pin, pin.data) is False:
                raise ValidationError('Wrong pin')
    

            
        
        


class EditProfileInfo(FlaskForm):
    """This is teh form fo rediting profile"""
    username = StringField('Username', validators=[DataRequired()])
    phonenumber = StringField('Phone number', validators=[DataRequired()])
    submit = SubmitField('Update information')

    def validate_phonenumber(self, phonenumber):
        """validate the phonenmber"""
        from app.models import Customer
        customer = Customer.query.filter_by(phone_number=phonenumber.data).first()
        if customer is not None and current_user.id != customer.user_id:
            raise ValidationError('Phonenumber already in use')
        phone_no = phonenumber.data
        if phonenumber.data[0] == 0:
            phone_no = phonenumber.data[1:]
        try:
            int(phone_no)
        except Exception:
            raise ValidationError('Phonenumber cannot be words')
        customer 

    
    def validate_username(self, username):
        """Validate username"""
        from app.models import Customer
        customer = Customer.query.filter_by(username=username.data).first()
        if customer is not None:
            raise ValidationError('Username already taken.')
        
class EditProfileAddress(FlaskForm):
    """This is to edit the address"""
    apartment_number = StringField('Apartment number', validators=[DataRequired(), Regexp(regex=r'\d*', message='Values must be digits')])
    street_name = StringField('Street name', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    postal_code = StringField('Postal Code', validators=[Regexp(regex=r'\d*', message='Values must be digits')])
    address_line_2 = StringField('Address Line 2')
    submit = SubmitField('Update Your Address')
    
class GenerateStatement(FlaskForm):
    """Class form for generating statements"""
    start = DateField('Start Date', validators=[DataRequired()])
    end = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('Generate Statement')


class VerifyPin(FlaskForm):
    """Class form for pin verification in changing pin"""
    pin = PasswordField('Input Pin', validators=[DataRequired(), Length(min=4, max=4)])
    verify = SubmitField('Verify')

    def validate_pin(self, pin):
        """Validate the pin"""
        from app.models import Account
        in_pin = pin.data
        account: Account = Account.query.filter_by(id=request.args.get('id')).first()
        if check_password_hash(account.account_pin, in_pin) is False:
            raise ValidationError('Pin inputed is incorrect')
        

class NewPin(FlaskForm):
    """Class form for pin verification in changing pin"""
    pin = PasswordField('Input New Pin', validators=[DataRequired(), Length(min=4, max=4)])
    change = SubmitField('Change Pin')

    def validate_pin(self, pin):
        try:
            int(pin.data)
        except Exception:
            raise ValidationError('The pin should be digits')
        
class CloseAccount(FlaskForm):
    """Form to delete your account"""
    acc_num = StringField('Input your account number', validators=[DataRequired(), Length(min=10, max=10)])
    dpin = PasswordField('Input Pin', validators=[DataRequired(), Length(min=4, max=4)])
    reason = SelectField('Why do you want to close your account?', choices=[
        ('I have a lot of accounts', 'I have a lot of accounts'), 
        ("I do not want to have a speedy account again", 'I do not want to have a speedy account again'),
        ('I want to open another speedy account', 'I want to open another speedy account'),
        ('I want to open another fintech account', 'I want to open another fintech account'),
        ('I am not satisfied with Speedy', 'I am not satisfied with speedy'),
        ('I do not have a reason', 'I do not have a reason')])
    close = SubmitField('Request Closure')
        
    def validate_acc_num(self, acc_num):
        """Validate the account number given"""
        from app.models import Account
        account: Account = Account.query.filter_by(account_number=self.acc_num.data).first()
        if account is None:
            raise ValidationError('Account number inputed does not exist')
        try:
            int(acc_num.data)
        except Exception:
            raise ValidationError('The account number should be digits')
    
    def validate_dpin(self, dpin):
        """Validate the pin"""
        from app.models import Account
        if self.acc_num.data == "":
            raise ValidationError('Please, input the account number')
        in_pin = dpin.data
        account: Account = Account.query.filter_by(account_number=self.acc_num.data).first()
        if account is not None:
            if check_password_hash(account.account_pin, in_pin) is False:
                raise ValidationError('Please, input the right pin')

class ChangeEmail(FlaskForm):
    """Change user email"""   
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Change Email')

class ChangePassword(FlaskForm):
    """Change user password"""
    old_password = PasswordField('Old Password', validators=[DataRequired()]) 
    new_password = PasswordField('New Password', validators=[DataRequired()]) 
    submit = SubmitField('Change Password')

    def validate_old_password(self, old_password):
        """Check to see if the inputed password is correct"""
        if check_password_hash(current_user.password_hash, old_password.data) is False:
            raise ValidationError('Wrong Pasword')
        
class DeleteAccount(FlaskForm):
    """Form to delete account"""
    password = PasswordField('Password', validators=[DataRequired()])
    delete = SubmitField('Delete My User Account', validators=[DataRequired()])


class ContactUs(FlaskForm):
    """Contact us flask form"""
    fullname = StringField('FULL NAME', validators=[DataRequired()])
    email = StringField('EMAIL ADDRESS', validators=[DataRequired(), Email()])
    subject = StringField('SUBJECT', validators=[DataRequired()])
    message = TextAreaField('MESSAGE', validators=[DataRequired()])
    submit = SubmitField('Send Message')