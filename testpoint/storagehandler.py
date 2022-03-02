from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from .storage import db
from .models import Person, Appointment, Result, User, Staff
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


def update_person(person_id: str, updates: dict) -> bool:
    """
    Updates a person information on the person table in the database if the person exists.
    :param person_id: Person ID as string.
    :param updates: User information dict with info to update.
    :return: True if person was updated, False if person to update does not exist.
    """
    person = get_person(person_id=person_id)
    if person is None:
        return False
    try:
        db.session.query(Person).filter(Person.person_id == person_id).update(updates)
    except IntegrityError as e:
        raise IntegrityError(statement=f"Duplicate encountered. {e.statement}",
                             params=e.params,
                             orig=e.orig)
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


def get_person(person_id: str) -> Optional[Person]:
    """
    Returns the person for the given person ID as a Person object as defined in models.
    :param person_id: Person ID of the requested user.
    :return: Person object as defined in database models.
    """
    person = Person.query.filter_by(person_id=person_id).first()
    return person if person else None


def appointment_exists(person_id: str, appointment_day: str, appointment_time: str) -> bool:
    """
    Check if a requested appointment for the given person and timeslot already exists in the database.
    :param person_id: ID of the person requesting an appointment.
    :param appointment_day: Date of appointment.
    :param appointment_time: Time of appointment.
    :return: True if appointment already exists, False otherwise.
    """
    appointment = Appointment.query.filter_by(person_id=person_id,
                                              appointment_day=appointment_day,
                                              appointment_time=appointment_time).first()
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
        raise TypeError(f"User {email} not found when trying to add appointment")
    if appointment_exists(person_id=person_id, appointment_day=appointment_day, appointment_time=appointment_time):
        return False

    appointment_id = token_urlsafe(nbytes=128)
    new_appointment = Appointment(appointment_id=appointment_id,
                                  person_id=person_id,
                                  appointment_day=appointment_day,
                                  appointment_time=appointment_time)
    db.session.add(new_appointment)
    db.session.commit()
    db.session.close()
    return True


def verify_appointment(appointment_id: str) -> bool:
    """
    Verifies an appointment by updating the verified column on the database table if appointment exists.
    :param appointment_id: Appointment ID as string.
    :return: True if appointment was updated, False if appointment does not exist.
    """
    appointment = get_appointment(appointment_id=appointment_id)
    if appointment is None:
        return False
    db.session.query(Appointment).filter(Appointment.appointment_id == appointment_id).update({'verified': 'Y'})
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


def get_appointment(appointment_id: str) -> Optional[Appointment]:
    """
    Returns the Appointment object for the given appointment ID.
    :param appointment_id: Appointment ID as string.
    :return: Appointment object with appointment_id.
    """
    appointment = Appointment.query.filter_by(appointment_id=appointment_id).first()
    return appointment if appointment else None


def get_appointment_by_key(key: str) -> Optional[Appointment]:
    """
    Returns the Appointment object for the given internal ID (primary key).
    :param key: Appointment internal ID as string.
    :return: Appointment object with ID.
    """
    appointment = Appointment.query.filter_by(id=key).first()
    return appointment if appointment else None


def get_verified_appointments() -> list[Appointment]:
    """
    Returns a list of all verified appointments that have no corresponding result.
    :return: List of verified appointments without result.
    """
    appointments = db.session.query(Appointment).join(Result, isouter=True).filter(and_(Appointment.verified == 'Y', Result.id.is_(None))).all()
    return appointments


def result_exists(appointment_id: str) -> bool:
    """
    Check if a result for the given appointment already exists in the database.
    :param appointment_id: ID of the person requesting an appointment.
    :return: True if result already exists, False otherwise.
    """
    result = Result.query.filter_by(appointment_id=appointment_id).first()
    return True if result else False


def add_result(appointment_id: str, person_id: str, result: str) -> bool:
    """
    Add result to database if appointment ID exists.
    :param appointment_id: Appointment ID as string.
    :param person_id: Person ID as integer.
    :param result: Test result as string.
    :return: True if result was added to database, False if result already exists.
    """
    if appointment_id is None:
        raise TypeError(f"No appointment ID given when trying to add result")
    if result_exists(appointment_id=appointment_id):
        raise RuntimeError(f"Result for person {person_id} was not added because a result already exists.")

    appointment = get_appointment(appointment_id=appointment_id)
    if not appointment:
        raise RuntimeError(f"Result for person {person_id} was not added because no corresponding appointment exists.")

    result_id = token_urlsafe(nbytes=128)
    new_result = Result(result_id=result_id,
                        appointment_id=appointment_id,
                        person_id=person_id,
                        result=result,
                        test_day=appointment.appointment_day,
                        test_time=appointment.appointment_time)
    db.session.add(new_result)
    db.session.commit()
    db.session.close()
    return True


def get_result_by_app_id(appointment_id: str) -> Optional[Result]:
    """
    Return Result object for given appointment ID.
    :param appointment_id: Appointment ID as string.
    :return: Result object or None if no such object exists.
    """
    result = Result.query.filter_by(appointment_id=appointment_id).first()
    return result if result else None


def get_user(username: str) -> Optional[User]:
    """
    Returns the User object for the given email address.
    :param username: Email address of user as string.
    :return: User object for username.
    """
    user = User.query.filter_by(username=username).first()
    return user if user else None


def get_user_pw(username: str) -> str:
    """
    Returns the password hash of a given user.
    :param username: Email address of the user as string.
    :return: Password hash for user with corresponding username/email address.
    """
    user = User.query.filter_by(username=username).first()
    return user.password


def get_staff(username: str) -> Optional[User]:
    """
    Returns the User object for the given email address.
    :param username: Email address of user as string.
    :return: User object for username.
    """
    staff = Staff.query.filter_by(username=username).first()
    return staff if staff else None


def is_admin(username: str) -> bool:
    """
    Checks whether user is an admin or not.
    :param username: Email address of user as string.
    :return: Role of user object for username.
    """
    staff = Staff.query.filter_by(email=username).first()
    return staff.admin == 'Y' if staff else False
