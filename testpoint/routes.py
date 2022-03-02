from flask import Blueprint, url_for, render_template, request, flash
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import redirect
from testpoint.models import Appointment, Person
from testpoint.notification import send_test_result_notification
from testpoint.storagehandler import is_admin, update_person, verify_appointment, get_verified_appointments, add_result, \
    get_appointment_by_key, get_person

routes = Blueprint('routes', __name__)


@routes.route("/appinfo/<app_id>", methods=['GET', 'POST'])
@login_required
def appinfo(app_id: str):
    """
    Check personal information of customers.
    :param app_id: Appointment ID as string.
    :return: User information template or redirect to login page.
    """
    appointment = Appointment.query.filter_by(appointment_id=app_id).first()
    person = Person.query.filter_by(person_id=appointment.person_id).first()
    if request.method == 'POST':
        user_input = request.form.to_dict()
        updates = {detail: user_input[detail] for detail in user_input if user_input[detail]}

        if not updates:
            verify_appointment(appointment_id=app_id)
            flash('Details verified!', category='success')
            return redirect(url_for('routes.staff'))
        try:
            update_person(person_id=person.person_id, updates=updates)
        except IntegrityError as e:
            flash(f"Could not update details. {e.statement}", category='error')
            return render_template('userinfo.html', appointment=appointment, person=person)

        verify_appointment(appointment_id=app_id)
        flash('Details updated successfully!', category='success')
        return redirect(url_for('routes.staff'))

    if appointment and person:
        return render_template('userinfo.html', appointment=appointment, person=person)
    return redirect(url_for('routes.staff'))


@routes.route("/admin/", methods=['GET', 'POST'])
@login_required
def admin():
    """
    Route for admin panel. Redirects to staff page if user is not admin.
    :return: Admin panel template if admin, otherwise staff page template.
    """
    if not is_admin(current_user.username):
        return redirect(url_for('routes.staff'))

    appointments = get_verified_appointments()
    if request.method == 'POST':
        appointment_id = request.form.get('appointment_id')
        test_result = request.form.get('test_result')
        appointment = get_appointment_by_key(key=appointment_id)
        person_id = appointment.person_id
        appointment_id = appointment.appointment_id
        try:
            add_result(appointment_id=appointment_id,
                       person_id=person_id,
                       result=test_result)
        except RuntimeError as e:
            flash(f"{e}", category='error')
            return redirect(url_for('routes.staff'))

        person = get_person(person_id=person_id)
        send_test_result_notification(email=person.email,
                                      first_name=person.first_name,
                                      appointment_id=appointment_id)
        flash('Added result and sent notification!', category='success')
        return render_template('admin.html', appointments=get_verified_appointments())

    return render_template('admin.html', appointments=appointments)


@routes.route("/staff/", methods=['GET', 'POST'])
@login_required
def staff():
    """
    Route for user center of staff.
    :return: HTML template for staff user center.
    """
    appointments = get_verified_appointments()
    if request.method == 'POST':
        appointment_key = request.form.get('appointment_key')
        test_result = request.form.get('test_result')
        appointment = get_appointment_by_key(key=appointment_key)
        person_id = appointment.person_id
        appointment_id = appointment.appointment_id
        try:
            add_result(appointment_id=appointment_id,
                       person_id=person_id,
                       result=test_result)
        except RuntimeError as e:
            flash(f"{e}", category='error')
            return redirect(url_for('routes.staff'))

        person = get_person(person_id=person_id)
        send_test_result_notification(email=person.email,
                                      first_name=person.first_name,
                                      appointment_id=appointment_id)
        flash('Added result and sent notification!', category='success')
        return render_template('staff.html', appointments=get_verified_appointments())

    return render_template('staff.html', appointments=appointments)
