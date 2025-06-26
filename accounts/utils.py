import uuid
from django.core.mail import send_mail
from django.conf import settings

def generateRandomToken():
    return str(uuid.uuid4())
def sendEmailToken(email , token):
    subject = "Verify Your Email Address"
    message = f"""Hi Please verify you email account by clicking this link 
    http://127.0.0.1:8000/accounts/verify-account/{token}
    
    """
    print("Calling token function...")
    token = generateRandomToken()
    print("Generated Token:", token)

    send_mail(
       subject,
       message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

def SendOtpToEmail(email , otp):
    subject = "Your OTP Code"
    message = f"""Hi, your OTP code is {otp}. Please use this code to verify your account.
    """
    send_mail(
       subject,
       message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

from django.utils.text import slugify
from .models import Hotel
def generateSlug(hotel_name):
    slug = f"{slugify(hotel_name)}-" + str(uuid.uuid4()).split('-')[0]
    if Hotel.objects.filter(hotel_slug = slug).exists():
        return generateSlug(hotel_name)
    return slug