from django.contrib.auth.models import User
from accounts import HotelVendor, Hotel  # <-- Replace with actual app name
from faker import Faker
from django.utils.text import slugify
import random

fake = Faker()

def seed_vendors_hotels_without_amenities(vendor_count=5, hotels_per_vendor=3):
    for _ in range(vendor_count):
        email = fake.email()
        username = email.split("@")[0]
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password="test1234"
        )

        vendor = HotelVendor.objects.create(
            user=user,
            phone_number=str(fake.phone_number()),
            business_name=fake.company()
        )

        for _ in range(hotels_per_vendor):
            name = fake.company()
            slug = slugify(name) + "-" + str(random.randint(1000, 9999))
            Hotel.objects.create(
                hotel_name=name,
                hotel_description=fake.paragraph(nb_sentences=3),
                hotel_location=fake.city(),
                hotel_price=round(random.uniform(1000, 5000), 2),
                hotel_owner=vendor,
                hotel_slug=slug,
                hotel_offer_price=round(random.uniform(800, 4500), 2),
                is_active=True
            )

    print("✅ Seeded vendors and hotels without amenities.")
