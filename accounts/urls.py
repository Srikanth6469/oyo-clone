

from django.urls import path
from accounts import views
from .views import verify_email_token


urlpatterns = [
   path("login/", views.login_page, name="login"),
   path("register/", views.register, name="registration"),
   path('send_otp/<email>/', views.send_otp, name='send_otp'),
   path('verify_otp/<email>/<otp>/', views.verify_otp, name='verify_otp'),
   path('verify-account/<token>/', verify_email_token, name="verify_email_token"),
   path("vendor/login_vendor/", views.login_vendor, name="login_vendor"),
   path("vendor/register_vendor/", views.register_vendor, name="vendor_registration"),
   path("vendor/vendor_dashboard/", views.vendor_dashboard, name="vendor_dashboard"),
   path("add_hotel/", views.add_hotel, name="addhotel"),
   path("vendor/upload_images/<hotel_slug>/", views.upload_images, name="upload_images"),
   path("vendor/delete_images/<id>/", views.delete_images, name="delete_images"),
   path('edit-hotel/<slug>/', views.edit_hotel , name="edit_hotel"),
   path("vendor_profile/", views.vendor_profile, name="vendor_profile"),
   path("logout_vendor/", views.logout_vendor, name="logout_vendor"),
   path("vendor/vendor_index/", views.vendor_index, name="vendor_index"),
   path("delete_hotel/<slug>/", views.delete_hotel, name="delete_hotel"),
   path("user_profile/", views.user_profile, name="user_profile"),
]
