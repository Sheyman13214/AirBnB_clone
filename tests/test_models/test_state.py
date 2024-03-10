#!/usr/bin/python3
"""This defines tests for models/state.py using unittest module.

Unittest classes:
    TestState_instantiation
    TestState_save
    TestState_to_dict
"""
import os
import models
import unittest
from time import sleep
from datetime import datetime
from models.state import State


class TestState_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the State class."""

    def test_no_args_instantiates(self):
        self.assertEqual(State, type(State()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(State().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_is_public_class_attribute(self):
        stat = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(stat))
        self.assertNotIn("name", stat.__dict__)

    def test_two_states_unique_ids(self):
        stat1 = State()
        stat2 = State()
        self.assertNotEqual(stat1.id, stat2.id)

    def test_two_states_different_created_at(self):
        stat1 = State()
        sleep(0.05)
        stat2 = State()
        self.assertLess(stat1.created_at, stat2.created_at)

    def test_two_states_different_updated_at(self):
        stat1 = State()
        sleep(0.05)
        stat2 = State()
        self.assertLess(stat1.updated_at, stat2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        stat = State()
        stat.id = "123456"
        stat.created_at = stat.updated_at = dtime
        statstr = stat.__str__()
        self.assertIn("[State] (123456)", statstr)
        self.assertIn("'id': '123456'", statstr)
        self.assertIn("'created_at': " + dtime_repr, statstr)
        self.assertIn("'updated_at': " + dtime_repr, statstr)

    def test_args_unused(self):
        stat = State(None)
        self.assertNotIn(None, stat.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dtime = datetime.today()
        dtime_iso = dtime.isoformat()
        stat = State(id="345", created_at=dtime_iso, updated_at=dtime_iso)
        self.assertEqual(stat.id, "345")
        self.assertEqual(stat.created_at, dtime)
        self.assertEqual(stat.updated_at, dtime)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_save(unittest.TestCase):
    """Tests for testing save method of the State class using unittest module."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        stat = State()
        sleep(0.05)
        first_updated_at = stat.updated_at
        stat.save()
        self.assertLess(first_updated_at, stat.updated_at)

    def test_two_saves(self):
        stat = State()
        sleep(0.05)
        first_updated_at = stat.updated_at
        stat.save()
        second_updated_at = stat.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        stat.save()
        self.assertLess(second_updated_at, stat.updated_at)

    def test_save_with_arg(self):
        stat = State()
        with self.assertRaises(TypeError):
            stat.save(None)

    def test_save_updates_file(self):
        stat = State()
        stat.save()
        statid = "State." + stat.id
        with open("file.json", "r") as file:
            self.assertIn(statid, file.read())


class TestState_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the State class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        stat = State()
        self.assertIn("id", stat.to_dict())
        self.assertIn("created_at", stat.to_dict())
        self.assertIn("updated_at", stat.to_dict())
        self.assertIn("__class__", stat.to_dict())

    def test_to_dict_contains_added_attributes(self):
        stat = State()
        stat.middle_name = "Holberton"
        stat.my_number = 98
        self.assertEqual("Holberton", stat.middle_name)
        self.assertIn("my_number", stat.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        stat = State()
        stat_dict = stat.to_dict()
        self.assertEqual(str, type(stat_dict["id"]))
        self.assertEqual(str, type(stat_dict["created_at"]))
        self.assertEqual(str, type(stat_dict["updated_at"]))

    def test_to_dict_output(self):
        dtime = datetime.today()
        stat = State()
        stat.id = "123456"
        stat.created_at = stat.updated_at = dtime
        tstdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dtime.isoformat(),
            'updated_at': dtime.isoformat(),
        }
        self.assertDictEqual(stat.to_dict(), tstdict)

    def test_contrast_to_dict_dunder_dict(self):
        stat = State()
        self.assertNotEqual(stat.to_dict(), stat.__dict__)

    def test_to_dict_with_arg(self):
        stat = State()
        with self.assertRaises(TypeError):
            stat.to_dict(None)


if __name__ == "__main__":
    unittest.main()
