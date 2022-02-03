import imp
from django.core.mail import EmailMessage
class Utils:
    @staticmethod
    def send_email(data):
        email=EmailMessage(subject=data['email_subject'], body = data['email_body'])
        email.send()