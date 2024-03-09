"""
this is the base model module
will hold the parent class
"""
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

import models
import uuid

if models.storage_type == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """
    the parent class for other classes
    """
    if models.storage_type == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """initialize the base model instance"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if kwargs:
            for k, v in kwargs.items():
                if k != "__class__":
                    setattr(self, k, v)

            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.fromisoformat(
                    kwargs.get("updated_at"))
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.fromisoformat(
                    kwargs.get("created_at"))

    def __str__(self):
        """string representation of the instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def to_dict(self):
        """return the dictionary of the instance"""
        obj_dict = self.__dict__.copy()

        if "updated_at" in obj_dict.keys():
            obj_dict["updated_at"] = obj_dict["updated_at"].isoformat()
        if "created_at" in obj_dict.keys():
            obj_dict["created_at"] = obj_dict["created_at"].isoformat()
        if "_sa_instance_state" in obj_dict.keys():
            del obj_dict["_sa_instance_state"]
        if "appointment_date" in obj_dict.keys():
            obj_dict["appointment_date"] = obj_dict["appointment_date"].isoformat()

        obj_dict["__class__"] = self.__class__.__name__
        return obj_dict

    def save(self):
        """add and save the instance"""
        self.updated_at = datetime.now()
        # add to storage if not there
        if not models.storage.get(self.__class__, self.id):
            models.storage.new(self)
        models.storage.save()

    def update(self, **kwargs):
        """update the instance"""
        if kwargs:
            for k, v in kwargs.items():
                if k not in ["id", "created_at", "updated_at", "__class__"]:
                    setattr(self, k, v)
            self.save()

    def delete(self):
        """delete the object"""
        models.storage.delete(self)
