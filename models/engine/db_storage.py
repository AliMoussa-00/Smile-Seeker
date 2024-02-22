"""this is the DB storage module"""

from models.base_model import Base, BaseModel
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBStorage:
    """Defining the DB storage class"""

    __engine = None
    __session = None
    __classes = {"BaseModel": BaseModel}

    def __init__(self):
        """Initializing the DB"""
        SS_DB_USER = getenv("SS_DB_USER")
        SS_DB_PWD = getenv("SS_DB_pwd")
        SS_DB_HOST = getenv("SS_DB_HOST")
        SS_DB = getenv("SS_DB")
        SS_DB_TYPE = getenv("SS_DB_TYPE")

        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
            SS_DB_USER, SS_DB_PWD, SS_DB_HOST, SS_DB
        ), pool_pre_ping=True)

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
            if cls is None or cls in self.__classes or cls is self.__classes[c]:
                for obj in self.__session.query(c).all():
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    objs[key] = obj
        
        return objs