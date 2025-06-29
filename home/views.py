from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from accounts.models import *


# Create your views here.
def index(request):
    hotels = Hotel.objects.all()
    if request.GET.get('search'):
        hotels = hotels.filter(hotel_name__icontains = request.GET.get('search'))

    if request.GET.get('sort_by'):
        sort_by = request.GET.get('sort_by')
        if sort_by == "sort_low":
            hotels = hotels.order_by('hotel_offer_price')
        elif sort_by == "sort_high":
            hotels = hotels.order_by('-hotel_offer_price')
    return render(request, 'index.html', context = {'hotels' : hotels[:50]})

from datetime import datetime

def hotel_details(request, slug):
    hotel = Hotel.objects.get(hotel_slug=slug)

    if request.method == "POST":
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            messages.error(request, "Invalid date format.")
            return HttpResponseRedirect(request.path_info)

        days_count = (end_date - start_date).days
        if days_count <= 0:
            messages.warning(request, "Invalid Booking Date.")
            return HttpResponseRedirect(request.path_info)
        try:
            hotel_user = HotelUser.objects.get(user=request.user)
            
        except HotelUser.DoesNotExist:
            messages.error(request, "User profile not found. Please complete your profile.")
            return HttpResponseRedirect(request.path_info)


        HotelBooking.objects.create(
            hotel=hotel,
            booking_user=hotel_user,
            booking_start_date=start_date,
            booking_end_date=end_date,
            price=hotel.hotel_offer_price * days_count
        )
        messages.success(request, "Booking Captured.")
        return HttpResponseRedirect(request.path_info)

    return render(request, 'hotel_detail.html', context={'hotel': hotel})
