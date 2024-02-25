"""this is the DB storage module"""

from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models.appointment import Appointments
from models.base_model import Base
from models.doctors import Doctors
from models.location import Location
from models.reviews import Reviews
from models.users import Users


class DBStorage:
    """Defining the DB storage class"""

    __engine = None
    __session = None
    __classes = {"Users": Users, "Doctors": Doctors, "Reviews": Reviews,
                 "Appointments": Appointments, "Location": Location}

    def __init__(self):
        """Initializing the DB"""
        SS_DB_USER = getenv("SS_DB_USER")
        SS_DB_PWD = getenv("SS_DB_pwd")
        SS_DB_HOST = getenv("SS_DB_HOST")
        SS_DB = getenv("SS_DB")

        self.__engine = create_engine("mysql+pymysql://{}:{}@{}/{}".format(
            SS_DB_USER, SS_DB_PWD, SS_DB_HOST, SS_DB
        ), pool_pre_ping=True)

        # !!!!! for testing
        # Base.metadata.drop_all(self.__engine)

    def reload(self):
        """creating a session and reloading db"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def all(self, cls=None):
        """get all the instances of a class or all in db"""

        objs = {}
        for c in self.__classes.keys():
            # if cls is None or cls is a string in classes or cls a class
            if cls is None or (cls in self.__classes.keys() and self.__classes[cls] is self.__classes[c]):
                for obj in self.__session.query(self.__classes[c]).all():
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    objs[key] = obj

        return objs

    def new(self, obj):
        """add a new object to the DB"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """save changes to the DB"""
        self.__session.commit()

    def get(self, cls, obj_id):
        """get a class instance based on id"""
        if cls and obj_id and obj_id != "":
            if cls in self.__classes.values():
                cls = cls.__name__
            if type(cls) is str and cls not in self.__classes:
                return None

            key = f"{cls}.{obj_id}"
            return self.all(cls).get(key, None)
        else:
            return None

    def delete(self, obj):
        """delete object from DB"""
        if obj:
            self.__session.delete(obj)

    def close(self):
        """close connection to the DB"""
        self.__session.remove()
