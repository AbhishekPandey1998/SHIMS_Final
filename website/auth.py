from typing import Literal
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user, LoginManager


auth = Blueprint('auth', __name__)

@auth.route('/patient-login', methods=['GET', 'POST'])
def patient_login():
    if request.method=='POST':
        health_id=request.form.get("health_id")
        password = request.form.get("password")

        user = User.query.filter_by(id=health_id).first()
        if(user and user.profession=="P"):
            if check_password_hash(user.password, password):
                flash('Logged in successfully !!!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.patient_dashboard'))
            else:
                flash('Incorrect password, try again !!!', category='error')
        else:
            flash('Patient does not exist', category='error')
    return render_template("patient_login.html", user=current_user)

@auth.route('/patient-signup', methods=['GET', 'POST'])
def patient_signup():
    if request.method=='POST':
        name = request.form.get("name")
        email = request.form.get("email")
        date_of_birth = request.form.get("date_of_birth")
        blood_group = request.form.get("blood_group")
        gender = request.form.get("gender")
        phone = request.form.get("phone")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Patient already exists', category='error')
        elif len(name)<2:
            flash('Full Name must be greater than 1 character',  category='error')
        elif password1!=password2:
            flash('Passwords don\'t match',  category='error')
        elif len(blood_group)>3:
            flash('Blood Group should not be more than 3 characters', category='error')
        elif len(gender)>1:
            flash('Gender should not be more than 1 character', category='error')
        elif len(password1)<7:
            flash('password must be greater than 7 characters.',  category='error')
        else:
            new_user = User(email=email, password = generate_password_hash(password1, method='sha256'), name=name, date_of_birth=date_of_birth, blood_group=blood_group, phone = phone, gender = gender, profession='P')
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Patient Account Created',  category='success')
            return redirect(url_for('views.patient_dashboard'))
    return render_template("patient_signup.html", user=current_user)

@auth.route('/doctor-login', methods=['GET', 'POST'])
def doctor_login():
    if request.method=='POST':
        doctor_id=request.form.get("doctor_id")
        password = request.form.get("password")

        user = User.query.filter_by(id=doctor_id).first()
        if(user and user.profession=="D"):
            if check_password_hash(user.password, password):
                flash('Logged in successfully !!!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.doctor_dashboard'))
            else:
                flash('Incorrect password, try again !!!', category='error')
        else:
            flash('Doctor does not exist', category='error')
    return render_template("doctor_login.html", user=current_user)

@auth.route('/doctor-signup', methods=['GET', 'POST'])
def doctor_signup():
    if request.method=='POST':
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        designation = request.form.get("designation")
        department = request.form.get("department")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Doctor already exists', category='error')
        elif len(name)<2:
            flash('Full Name must be greater than 1 character',  category='error')
        elif len(designation)<2:
            flash('Designation must be greater than 1 character',  category='error')
        elif len(department)<2:
            flash('Department must be greater than 1 character',  category='error')
        elif password1!=password2:
            flash('Passwords don\'t match',  category='error')
        elif len(password1)<7:
            flash('password must be greater than 7 characters.',  category='error')
        else:
            new_user = User(email=email, password = generate_password_hash(password1, method='sha256'), name=name, phone = phone, designation=designation, department=department, profession='D')
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Doctor Account Created',  category='success')
            return redirect(url_for('views.doctor_dashboard'))
    return render_template("doctor_signup.html", user=current_user)

@auth.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method=='POST':
        admin_id=request.form.get("admin_id")
        password = request.form.get("password")

        user = User.query.filter_by(id=admin_id).first()
        if(user and user.profession=="A"):
            if check_password_hash(user.password, password):
                flash('Logged in successfully !!!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.admin_dashboard'))
            else:
                flash('Incorrect password, try again !!!', category='error')
        else:
            flash('Admin does not exist', category='error')
    return render_template("admin_login.html", user=current_user)

@auth.route('/admin-signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method=='POST':
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        designation = request.form.get("designation")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Admin already exists', category='error')
        elif len(name)<2:
            flash('Full Name must be greater than 1 character',  category='error')
        elif len(designation)<2:
            flash('Designation must be greater than 1 character',  category='error')
        elif password1!=password2:
            flash('Passwords don\'t match',  category='error')
        elif len(password1)<7:
            flash('password must be greater than 7 characters.',  category='error')
        else:
            new_user = User(email=email, password = generate_password_hash(password1, method='sha256'), name=name, phone = phone, designation=designation, profession='A')
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Admin Account Created',  category='success')
            return redirect(url_for('views.admin_dashboard'))
    return render_template("admin_signup.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully !!!',  category='success')
    return redirect(url_for('views.home'))
