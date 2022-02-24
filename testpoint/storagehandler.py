from .storage import db
from .models import Person, Appointment
from typing import Optional
from secrets import token_urlsafe


def email_exists(email: str) -> bool:
    """
    Check if a person with given email exists in the database.
    :param email: Email address as a string.
    :return: True if person with given email exists, false otherwise.
    """
    person = Person.query.filter_by(email=email).first()
    return True if person else False


def person_exists(person: dict) -> bool:
    """
    Check if person with same name, birthdate and email address exists in database.
    :param person: Person as a dictionary.
    :return: True if person with same first name, last name, birthdate and email address exists, False otherwise.
    """
    if email_exists(email=person['email1']):
        return True
    person_db = Person.query.filter_by(first_name=person['first_name'],
                                       last_name=person['last_name'],
                                       birthdate=person['birthdate'],
                                       email=person['email1']).first()
    if person_db:
        if person['first_name'] != person_db.first_name:
            return False
        if person['last_name'] != person_db.last_name:
            return False
        if person['birthdate'] != person_db.birthdate.strftime("%Y-%m-%d"):
            return False
        if person['email1'] != person_db.email:
            return False
        return True
    return False


def add_person(person: dict) -> bool:
    """
    Adds a person to the person table in the database if the person does not exist already.
    :param person: Person as a dictionary.
    :return: True if person was added to the database, False if person already exists.
    """
    if person_exists(person=person):
        return False
    new_person = Person(last_name=person['last_name'],
                        first_name=person['first_name'],
                        email=person['email1'],
                        tel=person['tel'],
                        birthdate=person['birthdate'],
                        gender=person['gender'],
                        street=person['street'],
                        number=person['number'],
                        post_code=person['post_code'],
                        city=person['city'],
                        country=person['country'],
                        passport=person['passport'])
    db.session.add(new_person)
    db.session.commit()
    db.session.close()
    return True


def get_person_id(email: str) -> Optional[str]:
    """
    Returns the person ID of the person with the given email address.
    :param email: Email address as string.
    :return: Person_id as string or None.
    """
    person = Person.query.filter_by(email=email).first()
    return person.person_id if person else None


def appointment_exists(person_id: str, appointment_day: str, appointment_time: str) -> bool:
    """
    Check if a requested appointment for the given person and timeslot already exists in the database.
    :param person_id: ID of the person requesting an appointment.
    :param appointment_day: Date of appointment.
    :param appointment_time: Time of appointment.
    :return: True if appointment already exists, False otherwise.
    """
    appointment = Appointment.query.filter_by(person_id=person_id, appointment_day=appointment_day, appointment_time=appointment_time).first()
    return True if appointment else False


def add_appointment(email: str, appointment_day: str, appointment_time: str) -> bool:
    """
    Adds an appointment to the appointment table if the appointment does not already exist.
    :param email: Email address of user that requests an appointment.
    :param appointment_day: Date of appointment as string.
    :param appointment_time: Time of appointment as string.
    :return: True if a new appointment was added, False if appointment already exists.
    """
    person_id = get_person_id(email=email)
    if person_id is None:
        raise ValueError(f"User {email} not found when trying to add appointment")
    if appointment_exists(person_id=person_id, appointment_day=appointment_day, appointment_time=appointment_time):
        return False

    appointment_id = token_urlsafe(nbytes=32)
    new_appointment = Appointment(appointment_id=appointment_id,
                                  person_id=person_id,
                                  appointment_day=appointment_day,
                                  appointment_time=appointment_time)
    db.session.add(new_appointment)
    db.session.commit()
    db.session.close()
    return True


def get_appointment_id(person_id: str, appointment_day: str, appointment_time: str) -> Optional[str]:
    """
    Returns the appointment ID of the person with the given person ID.
    :param person_id: ID of the person that made the appointment as string.
    :param appointment_day: Date of the appointment as string.
    :param appointment_time: Time of the appointment as string.
    :return: Appointment ID as string or None.
    """
    appointment = Appointment.query.filter_by(person_id=person_id,
                                              appointment_day=appointment_day,
                                              appointment_time=appointment_time).first()
    return appointment.appointment_id if appointment else None


def calculate_available_time_slots(date: str) -> list[(str, str)]:
    """
    Calculates available time slots for appointments based on existing appointments.
    :param date: Day to check for available appointments.
    :return: List of available appointments.
    """
    all_slots = [dt.time(hour=h, minute=m) for h in range(8, 23) for m in [0, 15, 30, 45]]
    booked = Appointment.query.filter_by(appointment_day=date).all()
    booked_slots = [app.appointment_time for app in booked]
    return [slot for slot in all_slots if slot not in booked_slots]
