import datetime as dt
import re


def request_is_valid(request: dict) -> bool:
    """
    Checks if data in the given Request is valid.
    :param request: Flask Request object contain the data from the form.
    :return: True if the data adheres to the given rules, False otherwise.
    """
    if not date_is_valid(request['appointment_day']):
        raise ValueError("Please select a valid appointment date.")
    if not name_is_valid(request['first_name']) or not name_is_valid(request['last_name']):
        raise ValueError("Please provide a valid name.")
    if not email_is_valid(request['email1']):
        raise ValueError("Please provide a valid email address.")
    if request['email1'] != request['email2']:
        raise ValueError("Email addresses do not match. Please check your inputs.")
    if not tel_is_valid(request['tel']):
        raise ValueError("Please provide a valid telephone number with a country code (+49 for Germany).")
    if not birthdate_is_valid(request['birthdate']):
        raise ValueError("Please select a valid birthdate.")
    if not name_is_valid(request['street']):
        raise ValueError("Please provide a valid street name.")
    if not house_number_is_valid(request['number']):
        raise ValueError("Please provide a valid house number.")
    if not postcode_is_valid(request['post_code']):
        raise ValueError("Please provide a valid post code.")
    if not name_is_valid(request['city']):
        raise ValueError("Please provide a valid city name.")
    if not name_is_valid(request['country']):
        raise ValueError("Please provide a valid country name.")
    return True


def name_is_valid(name: str) -> bool:
    """
    Check if name is a valid string with only letters in it.
    :param name: Name as a string.
    :return: True if name contains only letters, False otherwise.
    """
    return all(x.isalpha() or x.isspace() for x in name) and len(name) > 1


def date_is_valid(date: str) -> bool:
    """
    Check whether given date is of format YYYY-MM-DD
    :param date: Date passed as string.
    :return: True if date has format YYYY-MM-DD, False otherwise.
    """
    if re.match("\\d{4}-\\d{2}-\\d{2}", date):
        return True
    return False


def email_is_valid(email: str):
    """
    Check if email address adheres to expected structure of an email address (prefix@domain).
    :param email: Email address as a string.
    :return: True if email is a valid email address, False otherwise.
    """
    if not re.match("[^@]+@[^@]+\\.[^@]+", email):
        return False
    return True


def birthdate_is_valid(birthdate: str) -> bool:
    """
    Check whether given birthdate has a valid format (YYYY-MM-DD) lies in the past.
    :param birthdate: Birthdate to check as string.
    :return: True if birthdate has expected format lies in the past, False otherwise.
    """
    if not date_is_valid(birthdate):
        return False
    try:
        birthdate_dt = dt.datetime.strptime(birthdate, "%Y-%m-%d")
    except ValueError as e:
        print("Birthdate has wrong format:", e)
        return False
    return birthdate_dt < dt.datetime.today()


def tel_is_valid(tel: str) -> bool:
    """
    Check if given telephone number is a valid number adhering to the format +XX XXX XXXXXXXX.
    :param tel: Telephone number as a string.
    :return: True if telephone number is a valid telephone number, False otherwise.
    """
    tel_no_spaces = ''.join(tel.split())
    if re.match("\\+\\d{11,14}", tel_no_spaces):
        return True
    return False


def house_number_is_valid(house_number: str) -> bool:
    """
    Checks if given house number is a valid house number in the format [number][optional letter].
    :param house_number: House number as a string.
    :return: True if house number has format [number][optional letter], False otherwise.
    """
    if re.match("\\d{1,4}[\\w]?", house_number):
        return True
    return False


def postcode_is_valid(postcode: str) -> bool:
    """
    Check if given postcode is a 5-digit number.
    :param postcode: Postcode as a string.
    :return: True if postcode is a 5-digit number, False otherwise.
    """
    if re.match("\\d{5}", postcode):
        return True
    return False
