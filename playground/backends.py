from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from .models import People

from django.core.signing import TimestampSigner
from django.core.mail import send_mail
from django.conf import settings

class PeopleAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            student = People.objects.get(username=username)
            if check_password(password, student.password):  # Compare hashed passwords
                student.backend = self.__class__.__module__ + '.' + self.__class__.__name__
                return student
            else:
                return None  # Authentication failure (wrong password)
        except People.DoesNotExist:
            return None  # User not found

    #Currently not working due to Google privacy issues, TODO...
    def generate_reset_token(email):
        signer = TimestampSigner()
        token = signer.sign(email)
        return token

    def send_password_reset_email(user):
        reset_token = user.reset_token  # Get the reset token from the user's record
        reset_link = f"{settings.BASE_URL}/reset-password/?token={reset_token}"

        subject = "Password Reset"
        message = f"Click the following link to reset your password:\n\n{reset_link}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)
