from flask import flash, render_template, redirect, request, url_for
from werkzeug.security import generate_password_hash
from flask_login import login_required

from EMS.admin import admin
from EMS import db
from EMS.models import User


@admin.route('/addemp', methods=['GET', 'POST'])
@login_required
def addemp():
    if request.method == 'POST':
        check_user = User.query.filter_by(email=request.form.get('email')).first()
        if check_user:
            flash('Email Already in use. Please try with another email', 'danger')
            return redirect(url_for('admin.addemp'))
        name = request.form.get('name')
        email = request.form.get('email')
        hash_password = generate_password_hash(request.form.get('password'))
        phone = request.form.get('phone')
        department = request.form.get('department')
        role = request.form.get('role')
        salary = request.form.get('salary')

        entry = User(name=name, email=email, password=hash_password, phone=phone, department=department, role=role, salary=salary)
        db.session.add(entry)
        db.session.commit()
        # This will add employee in the database.
        flash('Employee added successfully.', 'success')
        return redirect(url_for('home.adminhome'))

    return render_template('addemp.html')


@admin.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    if request.method == 'POST':
        emp = User.query.filter_by(id=id).first()
        emp.name = request.form['name']
        emp.phone = request.form['phone']
        emp.department = request.form['department']
        emp.role = request.form['role']
        emp.salary = request.form['salary']
        db.session.commit()
        # This will update's current employee's detail in the database.
        flash('Employee updated successfully.', 'success')
        return redirect(url_for('home.adminhome'))

    Emp = User.query.filter_by(id=id).first()
    return render_template("update.html", Emp=Emp)


@admin.route('/delete/<int:id>')
@login_required
def delete(id):
    emp = User.query.filter_by(id=id).first()
    db.session.delete(emp)
    db.session.commit()
    # This will delete current employee's detail from the database.
    flash('Employee deleted successfully.', 'success')
    return redirect(url_for('home.adminhome'))
