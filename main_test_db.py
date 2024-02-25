#!/usr/bin/python3
"""a main file to test tables in DB"""
from models import storage
from models.appointment import Appointments
from models.doctors import Doctors
from models.location import Location
from models.reviews import Reviews
from models.users import Users

u1_dict = {"first_name": "u1", "last_name": "lu1", "email": "u1@gmail.com", "password": "password",
           "phone": "+1225675674"}
u1 = Users(**u1_dict)
u1.save()

d1_dict = {"first_name": "d1", "last_name": "ld1", "email": "d1@gmail.com", "password": "password",
           "phone": "+1225675674"}
d1 = Doctors(**d1_dict)
d1.save()
d2_dict = {"first_name": "d2", "last_name": "ld2", "email": "d2@gmail.com", "password": "password",
           "phone": "+1225675674"}
d2 = Doctors(**d2_dict)
d2.save()

r1_dict = {"user_id": u1.id, "doctor_id": d1.id, "comment": "Good Doc", "rating": "5"}
r1 = Reviews(**r1_dict)
r1.save()
r2_dict = {"user_id": u1.id, "doctor_id": d1.id, "comment": "Good Doc", "rating": "5"}
r2 = Reviews(**r2_dict)
r2.save()
r3_dict = {"user_id": u1.id, "doctor_id": d2.id, "comment": "Good Doc", "rating": "5"}
r3 = Reviews(**r3_dict)
r3.save()
r4_dict = {"user_id": u1.id, "doctor_id": d2.id, "comment": "Good Doc", "rating": "5"}
r4 = Reviews(**r4_dict)
r4.save()

a1_dict = {"user_id": u1.id, "doctor_id": d1.id}
a1 = Appointments(**a1_dict)
a1.save()

a2_dict = {"user_id": u1.id, "doctor_id": d2.id}
a2 = Appointments(**a2_dict)
a2.save()

l1_dict = {"doctor_id": d1.id, "address": "mdiq-tetouan"}
l1 = Location(**l1_dict)
l1.save()
l2_dict = {"doctor_id": d2.id, "address": "mdiq-tetouan"}
l2 = Location(**l2_dict)
l2.save()

print("-" * 70)
print(f"=> len(user) = {len(storage.all('Users'))}")
print(f"=> len(doctors) = {len(storage.all('Doctors'))}")
print(f"=> len(reviews) = {len(storage.all('Reviews'))}")
print(f"=> len(appointments) = {len(storage.all('Appointments'))}")
print(f"=> len(location) = {len(storage.all('Location'))}")
print("=" * 70)

print(f"## len(user.reviews): {len(u1.reviews)}")
print(f"## len(doc.reviews): {len(d1.reviews)}")
print(f"## len(user.app): {len(u1.appointments)}")
print(f"## len(doc.app): {len(d1.appointments)}")
print(f"## len(doc.location): {len(d1.location)}")

print("=" * 30 + "user.reviews" + "=" * 30)
for r in u1.reviews:
    print(r.to_dict())

print("=" * 30 + "doctor.reviews" + "=" * 30)
for r in d1.reviews:
    print(r.to_dict())

print("=" * 30 + "user.appointments" + "=" * 30)
for a in u1.appointments:
    print(a.to_dict())

print("=" * 30 + "doctor.appointments" + "=" * 30)
for a in d1.appointments:
    print(a.to_dict())

print("Deleting Doctor_1: EXPECTED: reviews: 2, appointment: 1, locations: 1")
d2.delete()
print(f"=> len(user) = {len(storage.all('Users'))}")
print(f"=> len(doctors) = {len(storage.all('Doctors'))}")
print(f"=> len(reviews) = {len(storage.all('Reviews'))}")
print(f"=> len(appointments) = {len(storage.all('Appointments'))}")
print(f"=> len(location) = {len(storage.all('Location'))}")
