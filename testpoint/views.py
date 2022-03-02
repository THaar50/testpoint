from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from .validation import request_is_valid, birthdate_is_valid, email_is_valid
import datetime as dt
from .storagehandler import add_person, add_appointment, get_person_id, get_person, get_appointment, \
    get_result_by_app_id, is_admin
from .notification import send_booking_confirmation

views = Blueprint('views', __name__)


@views.route('/')
def home():
    """
    Defines route to the rendered template for the homepage. If the user is logged in it either looks like the
    admin panel or the user center.
    :return: HTML template for the homepage.
    """
    if current_user.is_authenticated:
        if is_admin(current_user.username):
            return redirect(url_for('routes.admin'))
        return redirect(url_for('routes.staff'))
    return render_template('home.html')


@views.route('/appointment/', methods=['GET', 'POST'])
def appointment() -> any:
    """
    Defines route to appointment booking page.
    :return: String of HTML template for appointment booking page or homepage if booking was successful.
    """
    if request.method == 'POST':
        user_input = request.form.to_dict()
        try:
            request_is_valid(request=user_input)
        except ValueError as e:
            flash(f"{e}", category='error')
            return render_template('appointment.html',
                                   user_input=user_input,
                                   slots=[dt.time(hour=h, minute=m) for h in range(8, 23) for m in [0, 15, 30, 45]],
                                   today=dt.date.today(),
                                   max_days=dt.date.today() + dt.timedelta(days=14))

        add_person(person=user_input)

        try:
            app_added = add_appointment(email=user_input['email1'],
                                        appointment_day=user_input['appointment_day'],
                                        appointment_time=user_input['appointment_time'])
        except TypeError as e:
            flash(f"{e}", category='error')
            return redirect(url_for('views.appointment'))
        if app_added:
            send_booking_confirmation(email=user_input['email1'],
                                      first_name=user_input['first_name'],
                                      appointment_day=user_input['appointment_day'],
                                      appointment_time=user_input['appointment_time'])
            flash('Appointment booked successfully! Please check your inbox for the booking confirmation.',
                  category='success')
        else:
            flash('Appointment is already booked! Please check your inbox for the booking confirmation.',
                  category='error')
        return redirect(url_for('views.home'))

    return render_template('appointment.html',
                           slots=[dt.time(hour=h, minute=m) for h in range(8, 23) for m in [0, 15, 30, 45]],
                           today=dt.date.today(),
                           max_days=dt.date.today()+dt.timedelta(days=14))


@views.route('/results/<app_id>/', methods=['GET', 'POST'])
def results(app_id: str) -> str:
    """
    Route to check a test result.
    :param app_id: Appointment ID to get the corresponding result of.
    :return: HTML templates for entering credentials,
    """
    if not get_appointment(appointment_id=app_id):
        return render_template('sorry.html')

    if request.method == 'POST':
        birthdate = request.form.get('birthdate')
        email = request.form.get('email_address')

        if not birthdate_is_valid(birthdate) or not email_is_valid(email):
            flash(f'No match for {birthdate} and {email}. Please check your inputs.', category='error')
            return render_template('results.html')

        person_id = get_person_id(email=email)
        if not person_id:
            flash(f'User {email} not found. Please check your inputs.', category='error')
            return render_template('results.html')

        person = get_person(person_id=person_id)
        if not person.email == email or not person.birthdate.strftime("%Y-%m-%d") == birthdate:
            flash('Email or birthdate is incorrect. Please try again.', category='error')
            return render_template('results.html')

        if not get_appointment(appointment_id=app_id):
            flash('Appointment not found. Please check your inputs.', category='error')
            return render_template('results.html')

        test_result = get_result_by_app_id(appointment_id=app_id)
        if not test_result:
            flash('No result available yet. Please wait.', category='error')
            return render_template('results.html')

        name = f"{person.first_name} {person.last_name}"
        post_code = person.post_code
        return render_template('testresult.html',
                               result=test_result.result,
                               name=name,
                               birthdate=birthdate,
                               post_code=post_code)
    return render_template('results.html')
