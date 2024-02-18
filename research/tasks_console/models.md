# Models

tasks for creating the models

`smile_seeker/models/`

## 1- create init.py

## 2- create Base Model:

- `def __init__(self, *args, **kwargs)`:
  
  - create a **new** instance or an existante one from a **dictionary** 
  
  - **id** : must be crypted (**uuid**) 
  
  - **create_at**: instance of **Date** if it is a **str** caste it back to **Date**
  
  - **update_at**: same

- `def __str__(self):`
  
  - return a string representation of an instance format:
    `[<class name>] (<self.id>) <self.__dict__>`

- `def to_dict(self):`
  
  - returns a dictionary containing all keys/values of the instance using **_str_**
  
  - **updated_at, created_at** : must be: 'Date' -> 'str: isoformat'

- `def save(self):`
  
  - save the instance if it updated
  
  - update **updated_at** with new Date
  
  - save the changes to **storage**

- `def update(self, **kwargs):`
  
  - update the instance with the **key**, **value** dictionary
  
  - and save the changes

- `def delete(self):`
  
  - delete the instance and remove it from storage

## 3- User.py

this the model to represent the regular user

- inherit from **BaseModel**

- class attributes
  
  - first name
  
  - last name
  
  - profile_picture
  
  - email
  
  - password **(hashed)**
  
  - phone

- `def __init__(self, *args, **kwargs):`
  
  - call `super().__init__(*args, **kwargs)`

## 4- Doctor.py

the is the model to represent the doctor instance

- inherit from **BaseModel**, **User**

- public class attributes:
  
  - Availability
  
  - location

- `def __init__(self, *args, **kwargs)`:
  
  - **id**, **created_at**, **updated_at**: will be created in the base Model

## 5- location.py

this the class for the doctor location

- inherit **BaseModel**

- class attributes
  
  - address => (Geocoding: convert address to latitude, longtitude ??)
  
  - latitude
  
  - longtitude
  
  - doctor_id

- `def __init__(self, *args, **kwargs):`
  
  - call `super().__init__(*args, **kwargs)`

## 6- Review

this is the model to represent the review class

- inherit from **BaseModel**

- class attributes
  
  - user_id
  
  - doctor_id
  
  - comment
  
  - rating

- `def __init__(self, *args, **kwargs):`
  
  - call `super().__init__(*args, **kwargs)`

## 7- Appointment

this is the class that will represent the appointement object

- inherit from **BaseModel**

- class attributes
  
  - user_id
  
  - doctor_id
  
  - appointment_date
  
  - status: (scheduled, confirmed, canceled)

- def **init**(self, *args, **kwargs):`
  
  - call `super().__init__(*args, **kwargs)`
