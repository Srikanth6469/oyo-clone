import email
from django.contrib.auth.models import User
from django.shortcuts import render ,redirect,get_object_or_404
from flask import request
from .models import HotelUser, HotelVendor, Hotel, Amenity , HotelImages
from django.db.models import Q
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .utils import generateRandomToken, sendEmailToken, SendOtpToEmail
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import random
#login for the hotel user--------------------------------------------------------------------------------------------
# def login_page(request):    
#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         hotel_user = HotelUser.objects.filter(
#             email = email)


#         if not hotel_user.exists():
#             messages.warning(request, "No Account Found.")
#             return redirect('/accounts/login/')

#         if not hotel_user[0].is_verified:
#             messages.warning(request, "Account not verified")
#             return redirect('/accounts/login/')

#         hotel_user = authenticate(username = hotel_user[0].username , password=password)

#         if hotel_user:
#             messages.success(request, "Login Success")
#             login(request , hotel_user)
#             messages.success(request, "Welcome to OYO Clone")
#             return redirect('index')

#         messages.warning(request, "Invalid credentials")
#         return redirect('/accounts/login/')
#     return render(request, 'login.html')
def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        hotel_user_qs = HotelUser.objects.filter(user__email=email)

        if not hotel_user_qs.exists():
            messages.warning(request, "No Account Found.")
            return redirect('/accounts/login/')

        hotel_user = hotel_user_qs[0]

        if not hotel_user.is_verified:
            messages.warning(request, "Account not verified.")
            return redirect('/accounts/login/')

        user = hotel_user.user
        authenticated_user = authenticate(username=user.username, password=password)

        if authenticated_user:
            login(request, authenticated_user)
            messages.success(request, "Login Success. Welcome to OYO Clone!")
            return redirect('index')

        messages.warning(request, "Invalid credentials.")
        return redirect('/accounts/login/')
    return render(request, 'login.html')


# Register for the hotel user--------------------------------------------------------------------------------------------
def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")
        
        hotel_user = HotelUser.objects.filter(
            Q(user__email=email) | Q(phone_number=phone_number)
        )
        
        if hotel_user.exists():
            messages.error(request, "User with this email or phone number already exists.")
            return redirect("registration")

        hotel_user = User.objects.create_user(
            
            username=phone_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
            
          
        )
        
        
        hotel_user = HotelUser.objects.create(
            user=hotel_user,
            phone_number=phone_number,
            email_token=generateRandomToken()
        )
        hotel_user.save()
        
        
        sendEmailToken(email, hotel_user.email_token)
        messages.success(request, "Verification email sent.")
        messages.success(request, "Registration successful.")
        
        return redirect("login")

    return render(request, "registration.html")



#email_verification--------------------------------------------------------------------------------------------

def verify_email_token(request, token):
    try:
        hotel_user = HotelUser.objects.get(email_token=token)
        hotel_user.is_verified = True
        hotel_user.save()
        messages.success(request, "Email verified")
        return redirect('/accounts/login/')
    except HotelUser.DoesNotExist:
        return HttpResponse("Invalid Token")

# send otp--------------------------------------------------------------------------------------------

def send_otp(request, email):
    hotel_user = HotelUser.objects.filter(
            email = email)
    if not hotel_user.exists():
            messages.warning(request, "No Account Found.")
            return redirect('/accounts/login/')

    otp =  random.randint(1000 , 9999)
    hotel_user.update(otp =otp)

    SendOtpToEmail(email , otp)

    return redirect(f'/accounts/verify_otp/{email}/{otp}/')
# verify otp--------------------------------------------------------------------------------------------

def verify_otp(request, email, otp):
    otp = request.POST.get('otp')
    hotel_user = HotelUser.objects.filter(email=email).first()
    
    if otp == hotel_user.otp:
        messages.success(request, "Login Success")
        login(request , hotel_user)
        return redirect('/accounts/login/')
    else:
        messages.error(request, "Invalid OTP.")
        messages.error(request, "User not found.")
        
    return render(request, 'verify_otp.html')

#vendor login--------------------------------------------------------------------------------------------

def login_vendor(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            vendor_profile = HotelVendor.objects.get(user__email=email)
        except HotelVendor.DoesNotExist:
            messages.warning(request, "No account found.")
            return redirect('/accounts/vendor/login_vendor/')

        if not vendor_profile.is_verified:
            messages.warning(request, "Account not verified.")
            return redirect('/accounts/vendor/login_vendor/')

        user_obj = vendor_profile.user

        user = authenticate(request, username=user_obj.username, password=password)

        if user:
            login(request, user)
            request.session['user_type'] = 'hotel_vendor'
            messages.success(request, "Login Success")
            return redirect('vendor_dashboard')

        messages.warning(request, "Invalid credentials")
        return redirect('/accounts/vendor/login_vendor/')

    return render(request, 'vendor/login_vendor.html')

#vendor registration---------------------------------------------------------------------------------------------------------------------
def register_vendor(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        business_name = request.POST.get("business_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")

        hotel_vendor = HotelVendor.objects.filter(
            Q(user__email=email) | Q(phone_number=phone_number)
        )

        if hotel_vendor.exists():
            messages.error(request, "User with this email or phone number already exists.")
            return redirect("vendor_registration")
        
        
        
        user = User.objects.create_user(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        hotel_vendor = HotelVendor.objects.create(
            user=user,
            phone_number=phone_number,
            business_name=business_name,
            email_token=generateRandomToken()
        )
        
        hotel_vendor.save()

        sendEmailToken(email, hotel_vendor.email_token)
        
        messages.success(request, "Verification email sent.")
        messages.success(request, "Registration successful.")
        return redirect("login_vendor")
    return render(request, "vendor/register_vendor.html")



#verify email token
def verify_email_token(request, token):
    try:
        hotel_vendor = HotelVendor.objects.get(email_token=token)
        hotel_vendor.is_verified = True
        hotel_vendor.save()
        messages.success(request, "Email verified")
        return redirect('/accounts/vendor/login_vendor/')
    except HotelVendor.DoesNotExist:
        return HttpResponse("Invalid Token")
#sendotp-----------------------hotelvendor
def send_otp(request, email):
    hotel_vendor = HotelVendor.objects.filter(
            user__email = email)
    if not hotel_vendor.exists():
            messages.warning(request, "No Account Found.")
            return redirect('/accounts/vendor/login_vendor/')

    otp =  random.randint(1000 , 9999)
    hotel_vendor.update(otp =otp)

    SendOtpToEmail(email , otp)

    return redirect(f'/accounts/verify_otp/{email}/{otp}/')
# verify otp------------------------------------------------------------------------------------

def verify_otp(request, email, otp):
    otp = request.POST.get('otp')
    hotel_vendor = HotelVendor.objects.filter(user__email=email).first()

    if otp == hotel_vendor.otp:
        messages.success(request, "Login Success")
        login(request , hotel_vendor)
        return redirect('vendor_dashboard')
    else:
        messages.error(request, "Invalid OTP.")
        messages.error(request, "User not found.")
    return render(request, 'verify_otp.html')

# vendor dashboard--------------------------------------------------------------------------------------------

@login_required(login_url=login_vendor)
def vendor_dashboard(request):
    try:
        vendor = request.user.hotel_vendor  # assuming related_name='hotel_vendor'
        hotels = Hotel.objects.filter(hotel_owner=vendor)
    except HotelVendor.DoesNotExist:
        hotels = []

    return render(request, "vendor/vendor_dashboard.html", {"hotels": hotels})

#addhotels-----------------------------------------------------------------------
@login_required(login_url=login_vendor)
def add_hotel(request):
    print("Amenities count in view:", Amenity.objects.all().count())
    if request.method == "POST":
        hotels = Hotel.objects.filter(hotel_owner=request.user.id)
        if hotels.count() >= 5:
            messages.error(request, "You can only add up to 5 hotels.")
            return redirect("vendor_dashboard")
        hotel_name = request.POST.get("hotel_name")
        hotel_description = request.POST.get("hotel_description")
        amenities = request.POST.getlist("amenities")
        hotel_price = request.POST.get("hotel_price")
        hotel_offer_price = request.POST.get("hotel_offer_price")
        hotel_location = request.POST.get("hotel_location")
        amenity_ids = request.POST.getlist('hotel_amenities[]')
        # hotel_vendor = HotelVendor.objects.get(user_ptr_id=request.user.id)
        from django.utils.text import slugify
        hotel_slug = slugify(hotel_name)
        try:
            hotel_vendor = HotelVendor.objects.get(user=request.user)
            print("Hotel Vendor:", hotel_vendor)
        except HotelVendor.DoesNotExist:
            # Handle the case: show error, redirect, or create a HotelVendor
            messages.error(request, "Vendor profile does not exist.")
            return redirect('addhotel')

        hotel_obj = Hotel.objects.create(
            hotel_name=hotel_name,
            hotel_description=hotel_description,
            hotel_price=hotel_price,
            hotel_offer_price=hotel_offer_price,
            hotel_location=hotel_location,
            hotel_slug=hotel_slug,
            hotel_owner=hotel_vendor,
            is_active=True,
            )


    
        amenity_ids = request.POST.getlist('hotel_amenities[]')
        for amenity_id in amenity_ids:
            amenity = Amenity.objects.get(id=amenity_id)    
            hotel_obj.amenities.add(amenity)
        hotel_obj.save()
        print(request.POST.getlist("hotel_amenities[]"))
        messages.success(request, "Hotel added successfully.")
        print("Hotel Object:", hotel_obj)
        return redirect("vendor_dashboard")

    amenities = Amenity.objects.all()
    return render(request, "addhotel.html", {'amenities': amenities})


# Image Upload---------------------------------------------------------------------------------------------
# This view allows the vendor to upload images for a specific hotel.
@login_required(login_url='login_vendor')

def upload_images(request, hotel_slug):
    hotel_obj = Hotel.objects.get(hotel_slug=hotel_slug)
    if request.method == "POST":

        image = request.FILES.get('image')
        print(image)
        if not image:
            messages.error(request, "No image selected.")
            return redirect(request.path_info)
        HotelImages.objects.create(
            hotel=hotel_obj,
            image=image
        )
        return HttpResponseRedirect(request.path_info)

    return render(request, 'vendor/upload_images.html', context={'images': hotel_obj.hotel_images.all()})

# This view allows the vendor to delete an image associated with a hotel.--------------------------------------------------------------------------
@login_required(login_url='login_vendor')
def delete_images(request, id):
    print(id)
    print("#######")
    hotel_image = HotelImages.objects.get(id = id)
    hotel_image.delete()
    messages.success(request, "Hotel Image deleted")
    return redirect('vendor_dashboard')

# Vendor Profile--------------------------------------------------------------------------------------------
def vendor_profile(request):
    is_vendor = HotelVendor.objects.filter(user=request.user).exists()
    vendor_profile = None

    if is_vendor:
        vendor_profile = HotelVendor.objects.get(user=request.user)

    return render(request, "vendor_profile.html", {
        "user": request.user,
        "is_vendor": is_vendor,
        "vendor_profile": vendor_profile,
    })
    
# logout vendor--------------------------------------------------------------------------------------------
def logout_vendor(request):
    logout(request)
    messages.success(request, "Logout Success")
    return redirect('index')

def vendor_index(request):
    return render(request, 'vendor/vendor_index.html')

    

@login_required(login_url='login_vendor')
def edit_hotel(request, slug):
    hotel_obj = Hotel.objects.get(hotel_slug=slug)
    
    # Check if the current user is the owner of the hotel
    if request.user != hotel_obj.hotel_owner:
        return HttpResponse("You are not authorized")

    if request.method == "POST":
        # Retrieve updated hotel details from the form
        hotel_name = request.POST.get('hotel_name')
        hotel_description = request.POST.get('hotel_description')
        hotel_price = request.POST.get('hotel_price')
        hotel_offer_price = request.POST.get('hotel_offer_price')
        hotel_location = request.POST.get('hotel_location')
        
        # Update hotel object with new details
        hotel_obj.hotel_name = hotel_name
        hotel_obj.hotel_description = hotel_description
        hotel_obj.hotel_price = hotel_price
        hotel_obj.hotel_offer_price = hotel_offer_price
        hotel_obj.hotel_location = hotel_location
        hotel_obj.save()
        
        messages.success(request, "Hotel Details Updated")

        return redirect('vendor_dashboard')

    # Retrieve amenities for rendering in the template
    amenities = Amenity.objects.all()

    # Render the edit_hotel.html template with hotel and amenities as context
    return render(request, 'vendor/edit_hotel.html', context={'hotel': hotel_obj, 'amenities': amenities})

def delete_hotel(request, slug):
    vendor = request.user.hotel_vendor 
    hotel_obj = get_object_or_404(Hotel, hotel_slug=slug, hotel_owner=vendor)

    hotel_obj.delete()
    messages.success(request, "Hotel deleted successfully.")
    return redirect("vendor_dashboard")


#user profile--------------------------------------------------------------------------------------------

def user_profile(request):
    return render(request, 'user_profile.html', {'user': request.user})

def vendor_dashboard(request):
    try:
        vendor = request.user.hotel_vendor  # assuming related_name='hotel_vendor'
        hotels = Hotel.objects.filter(hotel_owner=vendor)
    except HotelVendor.DoesNotExist:
        hotels = []

    return render(request, "vendor/vendor_dashboard.html", {"hotels": hotels})
