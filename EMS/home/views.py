from flask import render_template
from flask_login import login_required

from EMS.home import home
from EMS.models import User


@home.route('/')
def EMS():
    return render_template('ems.html')


@home.route('/adminhome', methods=['GET', 'POST'])
@login_required
def adminhome():
    Emps = User.query.all()
    return render_template('adminhome.html', Emps=Emps)


@home.route('/home')
@login_required
def home():
    return render_template('home.html')

