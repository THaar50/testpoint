import smtplib
import ssl
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from .config import EMAIL_SERVER, EMAIL_USER, EMAIL_PW, EMAIL_PORT
import qrcode
import io
from .storagehandler import get_person_id, get_appointment_id


def create_message(first_name: str, appointment_day: str, appointment_time: str):
    """
    Creates the HTML message for the email notification using first name and appointment details
    to personalize the message.
    :param first_name: First name of the user booking the appointment.
    :param appointment_day: Date of the appointment as string.
    :param appointment_time: Time of the appointment as string.
    :return: Personalized notification message for email notification.
    """
    message = f"""
                <html>
                    <body>
                        <h1>Thanks for booking your appointment!</h1>
                        <p>Hello {first_name}!</p>
                        <p>Thank you for booking an appointment for a Covid-19 test at the TestPoint test centre.</p>
                        <p>These are your booking details:</p>
                        <p>Date: {appointment_day}</p>
                        <p>Time: {appointment_time} Uhr</p>
                        <p>Place: TestPoint test centre Bonn, Münsterplatz.</p>
                        <p>Please show the below QRCode upon arrival at the test centre to get tested.</p>
                        <img src="cid:qrcode">
                    </body>
                </html>
                """
    return message


def create_qr_code(data: str) -> bytes:
    """
    Creates QRCode for given string.
    :param data: Data as string.
    :return: Bytes of the QRCode png image.
    """
    with io.BytesIO() as output:
        img = qrcode.make(data)
        img.save(output, format="png")
        return output.getvalue()


def send_mail(send_to: str, subject: str, message: str, appointment_id: str) -> None:
    """
    Send an email with given content.
    :param send_to: Recipient email address as string.
    :param subject: Subject of the email as string.
    :param message: Body of the email as html string.
    :param appointment_id: Appointment ID as string.
    :return: None
    """
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg_text = MIMEText(message, _subtype='html')
    msg.attach(msg_text)

    msg_img = MIMEImage(create_qr_code(appointment_id))
    msg_img.add_header('Content-ID', '<qrcode>')
    msg.attach(msg_img)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(EMAIL_SERVER, EMAIL_PORT, context=context) as server:
        server.login(EMAIL_USER, EMAIL_PW)
        server.sendmail(EMAIL_USER, send_to, msg.as_string())
        server.quit()


def send_booking_confirmation(email: str, first_name: str, appointment_day: str, appointment_time: str) -> None:
    """
    Sends a booking confirmation for the given email, name and appointment details.
    :param email: Email address of recipient as string.
    :param first_name: First name of the recipient as string.
    :param appointment_day: Date of the appointment as string.
    :param appointment_time: Time of the appointment as string.
    :return: None
    """
    person_id = get_person_id(email=email)
    appointment_id = get_appointment_id(person_id=person_id,
                                        appointment_day=appointment_day,
                                        appointment_time=appointment_time)
    message = create_message(first_name=first_name,
                             appointment_day=appointment_day,
                             appointment_time=appointment_time)
    subject = "Your booking confirmation for your appointment at TestPoint"
    send_mail(send_to=email, subject=subject, message=message, appointment_id=appointment_id)
