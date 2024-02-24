""" the user module """
import hashlib

from models.base_model import Base, BaseModel
from sqlalchemy import Column, String

import models


class Users(BaseModel, Base):
    """Defining the User class"""

    if models.storage_type == "db":
        __tablename__ = 'users'

        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        phone = Column(String(128), nullable=False)
        # picture = Column(String(128), nullable=True)

    else:
        first_name = ""
        last_name = ""
        email = ""
        password = ""
        phone = ""
        # picture = ""

    def __init__(self, *args, **kwargs):
        if kwargs.get("password", None) is not None:
            kwargs["password"] = self._hash_password(str(kwargs["password"]))
        super().__init__(*args, **kwargs)

    def _hash_password(self, password):
        # Hash the password using MD5
        hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()
        return hashed_password
