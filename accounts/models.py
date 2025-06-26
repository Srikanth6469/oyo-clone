from django.db import models
from django.contrib.auth.models import User 
from django.db import models
# from django.conf import settings

class HotelUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hotel_user')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    phone_number = models.CharField(unique=True, max_length=15, null=True, blank=True)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    class Meta:
        db_table = "hotel_user"
    def __str__(self):
        return f"{self.user.username} (Hotel User)"

class HotelVendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hotel_vendor')
    profile_picture = models.ImageField(upload_to='vendor_profile_pictures/', null=True, blank=True)
    phone_number = models.CharField(unique=True, max_length=15, null=True, blank=True)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    business_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "hotel_vendor"
    def __str__(self):
        return f"{self.user.username} (Hotel Vendor)"
        

class Amenity(models.Model):
    amenity_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    icon = models.ImageField(upload_to='amenity_icons/', null=True, blank=True)
    

    def __str__(self):
        desc = self.description[:30] if self.description else "No description"
        return f"{self.amenity_name} - {desc}"

class Hotel(models.Model):
    hotel_name = models.CharField(max_length=255)
    hotel_description = models.TextField()
    hotel_location = models.CharField(max_length=255)
    hotel_price = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = models.ManyToManyField(Amenity)
    hotel_owner = models.ForeignKey(HotelVendor, on_delete=models.CASCADE)
    hotel_slug = models.SlugField(max_length=255, unique=True)
    hotel_offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)

class HotelImages(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='hotel_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotel_images/')


class HotelManager(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    manager_name = models.CharField(max_length=255)
    manager_contact = models.CharField(max_length=15, null=True, blank=True)


class HotelBooking(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE , related_name="bookings" )
    booking_user = models.ForeignKey(HotelUser, on_delete = models.CASCADE , )
    booking_start_date = models.DateField()
    booking_end_date = models.DateField()
    price = models.FloatField()