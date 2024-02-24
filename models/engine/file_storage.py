"""create a file storage module"""

from models.base_model import BaseModel
from models.doctors import Doctors
from models.users import Users

import json


class FileStorage:
    __file_path = "file_storage.json"
    __objects = {}
    __classes = {"BaseModel": BaseModel, "User": Users, "Doctors": Doctors}

    def new(self, obj):
        """add a new object to '__objects' """
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """
        save an object into file.json
        using serialisation
        """
        json_dict = {}
        for k, v in self.__objects.items():
            json_dict[k] = v.to_dict()

        with open(self.__file_path, "w") as file:
            json.dump(json_dict, file)

    def reload(self):
        """deserialize json from file to '__objects'"""
        try:
            with open(self.__file_path, "r") as file:
                json_dict = json.load(file)

            if type(json_dict) is dict:
                for k, v in json_dict.items():
                    self.__objects[k] = self.__classes[v["__class__"]](**v)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def get(self, cls, obj_id):
        """get the instance of a class"""
        if cls:
            if cls in self.__classes.values():
                cls = cls.__name__
            if type(cls) is str and cls not in self.__classes:
                return None

            key = f"{cls}.{obj_id}"
            return self.__objects.get(key, None)
        else:
            return None

    def all(self, cls=None):
        """
        get all the instances in '__objects'
        or get only the instances of a specific class
        """
        if cls is None:
            return self.__objects.copy()
        else:
            if cls in self.__classes.values():
                cls = cls.__name__
            if type(cls) is str and cls not in self.__classes:
                return None

            objs = {}
            for k, v in self.__objects.items():
                if k.split(".")[0] == cls:
                    objs[k] = v
            return objs

    def delete(self, obj):
        """delete an obj"""
        if not obj:
            return

        key = f"{obj.__class__.__name__}.{obj.id}"
        if self.__objects.get(key, None):
            del self.__objects[key]

    def close(self):
        """reload data from file"""
        self.reload()
