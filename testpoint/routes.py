from flask import Blueprint, url_for, render_template, request, flash
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import redirect
from testpoint.models import Appointment, Person
from testpoint.storagehandler import is_admin, update_person

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
        updates = {key: user_input[key] for key in user_input if user_input[key]}

        if not updates:
            flash('Details verified!', category='success')
            return redirect(url_for('routes.staff'))
        try:
            update_person(person_id=person.person_id, updates=updates)
        except IntegrityError as e:
            flash(f"Could not update details. {e.statement}", category='error')
            return render_template('userinfo.html', appointment=appointment, person=person)

        flash('Details updated successfully!', category='success')
        return redirect(url_for('routes.staff'))

    if appointment and person:
        return render_template('userinfo.html', appointment=appointment, person=person)
    return redirect(url_for('auth.login'))


@routes.route("/admin/", methods=['GET', 'POST'])
@login_required
def admin():
    """
    Route for admin panel. Redirects to sorry page if user is not admin.
    :return: Admin panel template if admin, otherwise sorry page template.
    """
    if not is_admin(current_user.username):
        return render_template('sorry.html')
    return render_template('admin.html')


@routes.route("/staff/", methods=['GET', 'POST'])
@login_required
def staff():
    """
    Route for user center of staff.
    :return: HTML template for staff user center.
    """
    if request.method == 'POST':
        print('hello :3')
    return render_template('staff.html')
