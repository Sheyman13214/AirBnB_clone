#!/usr/bin/python3
"""This module creates the User class."""
from models.base_model import BaseModel

class User(BaseModel):
    """This is the class for managing objects of users."""

    email = ""  #empty string
    password = ""
    first_name = ""
    last_name = ""
