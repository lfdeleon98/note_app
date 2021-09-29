from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
#makes sure not to save password in plain text from security 
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        #check user email if valid
        user = User.query.filter_by(email=email).first()
        if user:
            #if the user exists, check password
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                #remembers that the user is logged in until the user clears their session
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        #if user doesnt exists
        else:
            flash('Account does not exist.', category='error')
    data = request.form
    print(data)
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #need to check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Account already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 8 characters.', category='error')
        else:
            #add user to the database
            #sha256 is a hashing algorithm
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account Created!', category='success')
            return redirect(url_for('views.home'))
            
    return render_template("sign_up.html", user=current_user)