"""
this is the base model module
will hold the parent class
"""
from datetime import datetime
import uuid


class BaseModel:
    """
    the parent class for other classes
    """
    def __init__(self, *args, **kwargs):
        """initialize the base model instance"""
        self.id = uuid.uuid4()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if kwargs:
            for k, v in kwargs.items():
                if k != "__class__":
                    setattr(self, k, v)

            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.fromisoformat(kwargs.get("updated_at"))
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.fromisoformat(kwargs.get("created_at"))

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

        obj_dict["__class__"] = self.__class__.__name__

        return obj_dict