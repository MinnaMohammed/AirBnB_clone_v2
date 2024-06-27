#!/usr/bin/python3
"""db engine"""
import json
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


Base = declarative_base()


class DBStorage:
    """ DBStorage engine """
    __engine = None
    __session = None

    def __init__(self):
        """ init method """
        HBNB_ENV = getenv('HBNB_ENV')
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_TYPE_STORAGE = getenv('HBNB_TYPE_STORAGE')
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(HBNB_MYSQL_USER, HBNB_MYSQL_PWD,
                                              HBNB_MYSQL_HOST, HBNB_MYSQL_DB),
                                      pool_pre_ping=True)
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """all method"""
        ObjList = {}
        if cls:
            ObjList = self.__session.query(cls).all()
        else:
            objectTypes = [User, State, City, Amenity, Place, Review]
            for c in objectTypes:
                ObjList.update(self.__session.query(c)).all()
        return ObjList

    def new(self, obj):
        """adds obj"""
        self.__session.add(obj)

    def save(self):
        """commit changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete method"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """reload method"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine),
                                        expire_on_commit=False)
