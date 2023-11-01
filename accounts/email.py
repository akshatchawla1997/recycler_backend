from .models import UserManager
from django.conf import settings
from django.core.mail import send_mail

def send_otp_via_email(email, otp):
    subject = "Your Account Verification E-Mail"
    message =  f"Hello,\nThank you for signing up with Kabadi Jee today.Kindly re-confirm your email address and activate your Kabadijiee by the OTP {otp}. This code expires in 10 Minutes.\n\nIf you didn't request this, contact support immediately.\n\nBest regards,\nThe Kabadijee Team"
    email_from = settings.EMAIL_HOST_USER
    recipients = [email]
    send_mail(subject, message, email_from, recipients)
