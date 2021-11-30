from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, send_file
from flask.helpers import flash, url_for
from werkzeug.utils import redirect
from .models import User, Report
from flask_login import login_required, current_user
from io import BytesIO
import json
from . import db
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/patient-landing')
def patient_landing():
    return render_template("patient_landing.html", user=current_user)

@views.route('/doctor-landing')
def doctor_landing():
    return render_template("doctor_landing.html", user=current_user)

@views.route('/admin-landing')
def admin_landing():
    return render_template("admin_landing.html", user=current_user)

@views.route('/patient-dashboard')
@login_required
def patient_dashboard():
    if(current_user.profession=="P"):
        return render_template("patient_dashboard.html", user=current_user)
    else:
        flash("You can't access the page without authorization !!!", 'error')
        return render_template("home.html", user=current_user)

@views.route('/patient-reports')
@login_required
def patient_reports():
    if(current_user.profession=="P"):
        return render_template("patient_reports.html", user=current_user)
    else:
        flash("You can't access the page without authorization !!!", 'error')
        return render_template("home.html", user=current_user)
    
@views.route('/doctor-dashboard')
@login_required
def doctor_dashboard():
    if(current_user.profession=="D"):
        return render_template("doctor_dashboard.html", user=current_user)
    else:
        flash("You can't access the page without authorization !!!", 'error')
        return render_template("home.html", user=current_user)

@views.route('/patient-details-and-reports')
@login_required
def patient_details_and_reports():
    if(current_user.profession=="D" or current_user.profession=="A" or current_user.profession=="P"):
        return render_template("patient_details_and_reports.html", user=current_user)
    else:
        flash("You can't access the page without authorization !!!", 'error')
        return render_template("home.html", user=current_user)
    
@views.route('/admin-dashboard')
@login_required
def admin_dashboard():
    if(current_user.profession=="A"):
        return render_template("admin_dashboard.html", user=current_user)
    else:
        flash("You can't access the page without authorization !!!", 'error')
        return render_template("home.html", user=current_user)
    
@views.route('/search-doctor', methods=['GET','POST'])
@login_required
def search_doctor():
    if request.method=='POST':
        search_doctor_id= request.form.get("search_doctor_id")
        
        doctor = User.query.filter_by(id=search_doctor_id).first()

        if (doctor and doctor.profession=='D'):
            return render_template("doctor_details.html", user=current_user, doctor=doctor)
        else:
            flash("Doctor with entered ID does not exist.", 'error')
            return render_template("search_doctor.html", user=current_user)
    elif(current_user.profession=="A"):
        return render_template("search_doctor.html", user=current_user)
    else:
        flash("You can't access the page without authorization !!!", 'error')
        return render_template("home.html", user=current_user)
    
@views.route('/edit-doctor-details', methods=['GET','POST'])
@login_required
def edit_doctor_details():
    if request.method=='POST':
        doctor_id=request.form.get("doctor_id")
        new_name=request.form.get("new_name")
        new_phone=request.form.get("new_phone")
        new_designation=request.form.get("new_designation")
        new_department=request.form.get("new_department")
        

        doctor = User.query.filter_by(id=doctor_id).first()

        if(doctor and doctor.profession=="D"):
            if(new_name!=""):
                doctor.name=new_name
                db.session.commit()
            if(new_phone!=""):
                doctor.phone=new_phone
                db.session.commit()
            if(new_designation!=""):
                doctor.designation=new_designation
                db.session.commit()
            if(new_department!=""):
                doctor.department=new_department
                db.session.commit()
            flash('Doctor details updated',  category='success')
            # return render_template("admin_dashboard.html", user=current_user)
            return redirect(url_for("views.admin_dashboard"))
        else:
            flash('Doctor with the entered ID does not exist',  category='error')
            return redirect(url_for("views.edit_doctor_details"))
    if(current_user.profession=="A"):
        return render_template("edit_doctor_details.html", user=current_user)
    else:
        flash("You can't access the page without authorization !!!", 'error')
        return render_template("home.html", user=current_user)
    
@views.route('/add-doctor')
@login_required
def add_doctor():
    if(current_user.profession=="A"):
        return render_template("add_doctor.html", user=current_user)
    else:
        flash("You can't access the page without authorization !!!", 'error')
        return render_template("home.html", user=current_user)
    
@views.route('/search-patient', methods=['GET', 'POST'])
@login_required
def search_patient():
    if request.method=='POST':
        search_health_id= request.form.get("search_health_id")
        
        patient = User.query.filter_by(id=search_health_id).first()

        if (patient and patient.profession=='P'):
            return render_template("patient_details_and_reports.html", user=current_user, patient=patient)
        else:
            flash("Patient with entered Health ID does not exist.", 'error')
            return render_template("search_patient.html", user=current_user)
    elif(current_user.profession=="A" or current_user.profession=="D" or current_user.profession=="P"):
        return render_template("search_patient.html", user=current_user)
    else:
        flash("You can't access the page without authorization !!!", 'error')
        return render_template("home.html", user=current_user)
    
@views.route('/upload-patient-reports',methods=['GET','POST'])
@login_required
def upload_patient_reports():
    if request.method=='POST':
        patient_id=request.form.get("patient_id")
        type_of_report=request.form.get("type_of_report")
        file = request.files['report']

        patient=User.query.filter_by(id=patient_id).first()
        if(patient and patient.profession=="P"):
            newReport = Report(patient_id=patient_id, type_of_report=type_of_report, file=file.read())
            db.session.add(newReport)
            db.session.commit()
            flash("Report "+file.filename+" uploaded successfully for patient ID: "+patient_id,'success')
        else:
            flash("No patient exists with the entered ID.",'error')
        return redirect(url_for("views.upload_patient_reports"))


    elif(current_user.profession=="A"):
        return render_template("upload_patient_reports.html", user=current_user)
    else:
        flash("You can't access the page without authorization !!!", 'error')
        return render_template("home.html", user=current_user)

@views.route('/delete-report', methods=['POST'])
def delete_report():
    report=json.loads(request.data)
    report_id = report['report_id']
    report=Report.query.get(report_id)
    if report and current_user.profession=='A':
        flash('Report deleted !!!','success')
        db.session.delete(report)
        db.session.commit()
    return jsonify({})

@views.route('/download-report',methods=['POST'])
def download_report():
    report=json.loads(request.data)
    report_id = report['report_id']
    report=Report.query.get(report_id)
    if report:
        return send_file(BytesIO(report.file), attachment_filename=report.type_of_report+"_"+str(report.patient_id)+".pdf" , as_attachment=True)
    return jsonify({})
