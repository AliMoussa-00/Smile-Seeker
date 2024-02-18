# Engine

this is the model to represent the **storage** : (**FileStorage**, **DBStorage**)

## 1- init

## 2- file_storage.py

the file storage will be used for **serializing** instances to a **JSON** file
and **deserializing** back to instances

`models/engine/file_storage.py`

- `class FileStorage()`

- classe attributes:
  
  - `__objects`: a dictionary to hold all the instances
  
  - `__file_path`: a path to the json file **file.json**

- `def all(self, cls=None)` 
  get all the instances of all classes if cls is None OR get the instances of a single class

- `def new(self)`
  add in **__objects** the obj with key `<obj class name>.id`

- `def save(self)`
  serializes **__objects** to the JSON file

- `def reload(self)`
  deserializes the JSON file to __objects

- `def delete(self)`
  delete obj from **__objects** if it is in there

- `def close(self)`
  call reload() method for deserializing the JSON file to objects

- `def get(self, cls, id)`
  Returns the object based on the class name and its ID, or None if not found

- `def count(self, cls=None)`
  count the number of objects in storage

## 3- db_storage.py

creating and intgrating the **mariaDB** **DBMS** 

`!! change the models to create tables and thier columns`

#### 1- setup development

create a script.sql to setup the mariadb for : **dev**:

- A database ss_dev_db

- A new user ss_dev (in localhost)

- The password of ss_dev should be set to ss_dev_pwd

- ss_dev should have all privileges on the database ss_dev_db

- ss_dev should have SELECT privilege on the database performance_schema

- If the database ss_dev_db or the user ss_dev already exists, your script should not fail

create a script.sql to setup the mariadb for : **test**

- A database ss_test_db

- A new user ss_test (in localhost)

- The password of ss_test should be set to ss_test_pwd

- ss_test should have all privileges on the database ss_test_db

- ss_test should have SELECT privilege on the database performance_schema 

- If the database ss_test_db or the user ss_test already exists, your script should not fail

### 2- Update Models

update the models to use the DB storage

- Update `BaseModel: (models/base_model.py)`
  
  - `!!` create: `Base = declarative_base()` before the declaration of BaseModel
    
    **if** the **storage_type** == 'db'
  
  - in class **BaseModel** add **fields** for the attributes:
    
    - `id`: unique string, not Null, PK
    - created_at: datetime, not null
    - update_at: datetime, not null

- Update `models/user.py`
  
  - add table columns if `storage_type == 'db'`
    
    - first name: string, not null
    
    - last name: string, not null
    
    - profile_picture: BLOB, optional
    
    - email: string, not null
    
    - password: string hashed, not null
    
    - `reviews = relationship("Review", backref="user", cascade="all, delete, delete-orphan)`
    
    - `appointment = relationship("Appointment", backref="user", cascade="all, delete, delete-orphan)``

- Update `models/doctor.py`
  
  - add table columns if `storage_type == 'db'`
    
    - availability: boolean, default: True, not null
    
    - `location = 
      relationship("Location", backref="doctor", cascade="all, delete, delete-orphan)`

- Update `models/location.py`
  
  - add table columns if `storage_type == 'db'`
    
    - address: string, not null
    - longtitude: float, not null
    - latitude: float, not null
    - doctor_id: string, **FK**, not null

- Update `models/review.py`
  
  - add table columns if `storage_type == 'db'`
    
    - user_id: string **FK**
    
    - doctor_id: string **FK**
    
    - comment: string
    
    - rating: integer

- Update `models/appointment.py`
  
  - add table columns if `storage_type == 'db'`
    
    - user_id: string **FK**
    
    - doctor_id: string **FK**
    
    - appointment_date: datetime
    
    - status: (scheduled, confirmed, canceled): string, not null
