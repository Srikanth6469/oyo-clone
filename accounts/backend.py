from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import HotelUser, HotelVendor

class HotelAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, user_type=None, **kwargs):
        User = get_user_model()  # Gets the User model (django.contrib.auth.models.User)
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                # Check the user_type and related model
                if user_type == 'hotel_user' and hasattr(user, 'hotel_user'):
                    return user if user.hotel_user.is_verified else None
                elif user_type == 'hotel_vendor' and hasattr(user, 'hotel_vendor'):
                    return user if user.hotel_vendor.is_verified else None
                return None  # Wrong user_type or no related model
            return None  # Invalid password
        except User.DoesNotExist:
            return None  # User not found

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None