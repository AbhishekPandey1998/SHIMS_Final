from sqlalchemy.sql.expression import null
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Report(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type_of_report = db.Column(db.String(256))
    generation_date = db.Column(db.DateTime(timezone=True), default=func.now())
    file = db.Column(db.LargeBinary)
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    date_of_birth = db.Column(db.String(10), nullable=True)
    blood_group = db.Column(db.String(3), nullable=True)
    gender = db.Column(db.String(6), nullable=True)
    phone = db.Column(db.String(12))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    profession = db.Column(db.String(1))
    designation = db.Column(db.String(25), nullable=True)
    department = db.Column(db.String(60), nullable=True)
    reports = db.relationship('Report')
    def get_id(self):
        return self.id