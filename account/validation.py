from django.core import validators

class Validator:
    def username(username):
        if not username.endswith('@gmail.com'):
            raise validators.ValidationError('Domain name should be @gmail.com')

    def mobile(phone):
        if not phone.isdigit():
            raise validators.ValidationError("Enter correct mobile number")

        if not len(phone) == 10:
            raise validators.ValidationError('Moblie number is not correct')