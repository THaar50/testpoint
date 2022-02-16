from flask import Blueprint, render_template, request, flash, redirect, url_for

views = Blueprint('views', __name__)


@views.route('/')
def home() -> str:
    return render_template('home.html')


@views.route('/appointment/', methods=['GET', 'POST'])
def make_appointment() -> any:
    if request.method == 'POST':
        email1 = request.form.get('email1')
        email2 = request.form.get('email2')

        if email1 != email2:
            flash('E-Mail-Adressen stimmen nicht überein', category='error')
        else:
            flash('Terminanfrage erfolgreich verarbeitet. Bitte überprüfen Sie ihr Postfach für die Buchungsbestätigung.',
                category='success')

            return redirect(url_for('views.home'))

    return render_template('appointment.html')