#!/usr/bi/python3
"""This is the script for the base model of the AirBnB clone."""

import uuid
from models import storage
from datetime import datetime


class BaseModel:
    """This is the base class from which all other classes will inherit."""

    def __init__(self, *args, **kwargs):
        """This initializes instance attributes

        Args:
            - *args: A list of arguments (not used in this implementation)
            - **kwargs: A dict of key-values arguments
        """

        if kwargs is not None and kwargs != {}:  # Check if kwargs is not empty
            for key in kwargs:
                # Handle special cases for 'created_at' and 'updated_at'
                if key == "created_at":
                    # Convert the 'created_at' datetime string to a datetime object
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    # Convert the 'updated_at' datetime string to a datetime object
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    # Handle other attributes
                    self.__dict__[key] = kwargs[key]

        else:
             # Create a new instance with default values
             self.id = str(uuid.uuid4())
             self.created_at = datetime.now()
             self.updated_at = datetime.now()
             storage.new(self)

    def __str__(self):
        """Returns the official string representation"""

        return "[{}] ({}) {}".\
                format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """This updates the public instance attribute updated_at"""

        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """This returns a dictionary containing all keys/values of __dict__"""

        own_dict = self.__dict__.copy()
        own_dict["__class__"] = self.__class__.__name__
        own_dict["created_at"] = own_dict["created_at"].isoformat()
        own_dict["updated_at"] = own_dict["updated_at"].isoformat()
        return own_dict
