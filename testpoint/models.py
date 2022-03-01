from flask_login import UserMixin
from sqlalchemy import func
from .storage import db


class Person(db.Model):
    person_id = db.Column('person_id', db.Integer(), primary_key=True)
    last_name = db.Column('last_name', db.String(100), default=None)
    first_name = db.Column('first_name', db.String(100), default=None)
    email = db.Column('email', db.String(50), unique=True)
    tel = db.Column('tel', db.String(15), default=None)
    birthdate = db.Column('birthdate', db.Date, default=None)
    gender = db.Column('gender', db.String(1), default=None)
    street = db.Column('street', db.String(100), default=None)
    number = db.Column('number', db.String(5), default=None)
    post_code = db.Column('post_code', db.String(5), default=None)
    city = db.Column('city', db.String(50), default=None)
    country = db.Column('country', db.String(50), default=None)
    passport = db.Column('passport_number', db.String(10), default=None)
    created_at = db.Column('created_at', db.DateTime, default=func.now())
    appointments = db.relationship('Appointment')
    results = db.relationship('Result')


class Appointment(db.Model):
    id = db.Column('id', db.Integer(), primary_key=True)
    appointment_id = db.Column('appointment_id', db.String(150), unique=True)
    person_id = db.Column('person_id', db.Integer(), db.ForeignKey('person.person_id'))
    appointment_day = db.Column('appointment_day', db.Date, default=None)
    appointment_time = db.Column('appointment_time', db.Time, default=None)
    verified = db.Column('verified', db.String(1), default='N')
    created_at = db.Column('created_at', db.DateTime, default=func.now())
    result = db.relationship('Result')


class Result(db.Model):
    id = db.Column('id', db.Integer(), primary_key=True)
    result_id = db.Column('result_id', db.String(150), unique=True)
    appointment_id = db.Column('appointment_id', db.String(150), db.ForeignKey('appointment.appointment_id'), unique=True)
    person_id = db.Column('person_id', db.Integer(), db.ForeignKey('person.person_id'))
    result = db.Column('result', db.String(8), default=None)
    test_day = db.Column('test_day', db.Date, default=None)
    test_time = db.Column('test_time', db.Time, default=None)
    created_at = db.Column('created_at', db.DateTime, default=func.now())


class Staff(db.Model):
    id = db.Column('id', db.Integer(), primary_key=True)
    last_name = db.Column('last_name', db.String(100), default=None)
    first_name = db.Column('first_name', db.String(100), default=None)
    email = db.Column('email', db.String(50), unique=True)
    tel = db.Column('tel', db.String(15), default=None)
    birthdate = db.Column('birthdate', db.Date, default=None)
    admin = db.Column('admin', db.String(1), default='N')
    created_at = db.Column('created_at', db.DateTime, default=func.now())
    users = db.relationship('User')


class User(db.Model, UserMixin):
    id = db.Column('id', db.Integer(), primary_key=True)
    username = db.Column('username', db.String(50), db.ForeignKey('staff.email'))
    password = db.Column('password', db.String(300), default=None)
    created_at = db.Column('created_at', db.DateTime, default=func.now())
