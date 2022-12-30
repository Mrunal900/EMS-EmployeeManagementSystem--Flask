from flask import render_template, flash, redirect
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from EMS.auth.forms import RegistrationForm, LoginForm

from EMS.auth import auth
from EMS import db
from EMS.models import User


@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        check_user = User.query.filter_by(email=form.email.data).first()
        if check_user:
            flash('Email Already in use. Please try with another email and username', 'danger')
            return redirect('/register')
        password = generate_password_hash(form.password.data)
        user = User(name=form.name.data, email=form.email.data, password=password)
        db.session.add(user)
        db.session.commit()
        # This will add/register new employee to the database.
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect('/login')
    return render_template('register.html', form=form)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # This will check whether the employee exists in the database and whether
        # and the password entered matches the password in the database
        if user is not None and check_password_hash(user.password, form.password.data):
            if user.is_admin:
                login_user(user)
                return redirect('/adminhome')
            # if the user is admin this will redirect us to the Admin-home.
            else:
                login_user(user)
                return redirect('/home')
            # if the user is not admin this will redirect us to the Admin-home
        else:
            # if login details (email and password) are wrong.
            logout_user()
            flash('Login Unsuccessful. Please check username and password', 'danger')
            return redirect('/login')
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # this will log out the user and redirect us to the login page.
    flash('You have successfully been logged out.', 'success')
    return redirect('/login')


@auth.route('/profile')
@login_required
def profile():
    # This will show's the employee details
    if current_user.department is None and current_user.role is None:
        flash('You have successfully register, now your employer will update your information. If your not employee '
              'of this company your account will be deleted.', 'primary')
        return render_template('profile.html')
    return render_template('profile.html')
