from flask import Blueprint, render_template, request, flash, redirect, url_for
from .validation import request_is_valid
import datetime as dt
from .storagehandler import add_person, add_appointment
from .notification import send_booking_confirmation

views = Blueprint('views', __name__)


@views.route('/')
def home() -> str:
    """
    Defines route to the rendered template for the homepage.
    :return: String of HTML template for the homepage.
    """
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
            return redirect(url_for('views.appointment'))

        add_person(person=user_input)

        try:
            app_added = add_appointment(email=user_input['email1'],
                                        appointment_day=user_input['appointment_day'],
                                        appointment_time=user_input['appointment_time'])
        except ValueError as e:
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
