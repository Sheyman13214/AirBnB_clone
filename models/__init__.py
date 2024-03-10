#!/usr/bin/python3
"""This initializes the Python package"""
from models.engine.file_storage import FileStorage
storage = FileStorage()
storage.reload()
