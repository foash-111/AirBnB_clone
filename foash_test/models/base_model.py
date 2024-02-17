#!/usr/bin/python3
"""main module for base class
    """

import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """main class for this projecta
    """

    def __init__(self, *args, **kwargs):
        """constructor

        Args:
            id (__type__, str): generated by (uuid) & converted to str
            created_at (_type_, str): time obj created. Defaults to None.
            updated_at (_type_, str): time obj updated. Defaults to None.
        """
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
        else:
            self.id = kwargs.get("id")
            self.created_at = datetime.fromisoformat(kwargs.get("created_at"))
            self.updated_at = datetime.fromisoformat(kwargs.get("updated_at"))
            for key, value in kwargs.items():
                if key not in self.__dict__.keys():
                    self.__dict__[key] = value

    def __str__(self):
        """string representation of an object"""
        return f"[{__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """updates the public instance attribute
        updated_at with the current datetime"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """returns a dictionary containing all
        keys/values of __dict__ of the instance
        """
        new_dict = {}
        new_dict = self.__dict__
        new_dict["__class__"] = __class__.__name__
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        return new_dict
