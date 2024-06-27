#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    citiesList = []
    if getenv("HBNB_MYSQL_TYPE_STORAGE") == "db":
        cities = relationship("City", backref="state",
                              cascade="all, delete, delete-orphan")
    elif getenv("HBNB_MYSQL_TYPE_STORAGE") == "file":
        @property
        def cities(self):
            """getter"""
            from models import storage
            citiesList = []
            for k in storage.all("City").values():
                if city.state_id == self.id:
                    citiesList.append(k)
            return citiesList
