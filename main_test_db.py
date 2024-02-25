#!/usr/bin/python3
"""a main file to test tables in DB"""
from models import storage

from models.appointment import Appointments
from models.doctors import Doctors
from models.users import Users
from models.reviews import Reviews

u1_dict = {"first_name": "u1", "last_name": "lu1", "email": "u1@gmail.com", "password": "password", "phone": "+1225675674"}
u1 = Users(**u1_dict)
u1.save()

d1_dict = {"first_name": "d1", "last_name": "ld1", "email": "d1@gmail.com", "password": "password", "phone": "+1225675674"}
d1 = Doctors(**d1_dict)
d1.save()
d2_dict = {"first_name": "d2", "last_name": "ld2", "email": "d2@gmail.com", "password": "password", "phone": "+1225675674"}
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

print("-" * 30)
print(f"=> user.len = {len(storage.all('Users'))}")
print(f"=> doctors.len = {len(storage.all('Doctors'))}")
print(f"=> reviews.len = {len(storage.all('Reviews'))}")
print(f"=> appointments.len = {len(storage.all('Appointments'))}")
print("-" * 30)

print("Deleting Doctor_1: EXPECTED: reviews: 2, appointment: 1")
d2.delete()
print(f"=> user.len = {len(storage.all('Users'))}")
print(f"=> doctors.len = {len(storage.all('Doctors'))}")
print(f"=> reviews.len = {len(storage.all('Reviews'))}")
print(f"=> appointments.len = {len(storage.all('Appointments'))}")





