"""the doctor module"""
import hashlib

from sqlalchemy import Column, String, LargeBinary
from sqlalchemy.orm import relationship, backref

from models import storage_type
from models.base_model import Base, BaseModel


class Doctors(BaseModel, Base):
    """Defining the doctors class"""

    if storage_type == "db":
        __tablename__ = 'doctors'

        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        email = Column(String(128), unique=True, nullable=False)
        password = Column(String(128), nullable=False)
        phone = Column(String(128), nullable=False)
        picture = Column(String(128), nullable=True)
        availability = Column(String(20), default="True")
        reviews = relationship("Reviews", backref="doctor", cascade="all, delete-orphan")
        appointments = relationship("Appointments", backref="doctor", cascade="all, delete-orphan")

        # one-to-one relationship with the location table
        location = relationship("Location", backref=backref("doctor", uselist=False), cascade="all, delete-orphan")

    else:
        availability = "True"

    def __init__(self, *args, **kwargs):
        """Initializing the doctors instance"""
        if kwargs.get("password", None) is not None:
            kwargs["password"] = self._hash_password(str(kwargs["password"]))
        super().__init__(*args, **kwargs)

    def _hash_password(self, password):
        # Hash the password using MD5
        hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()
        return hashed_password
