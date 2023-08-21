#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.amenity import Amenity
from models.base_model import BaseModel
from datetime import datetime
from unittest.mock import patch
from time import sleep
from os import getenv
import pycodestyle
import inspect
import unittest
storage_t = getenv("HBNB_TYPE_STORAGE")


class test_Amenity(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_name2(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)


class Test_PEP8(unittest.TestCase):
    """test User"""

    def test_pep8_user(self):
        """test pep8 style"""
        pep8style = pycodestyle.StyleGuide(quiet=True)
        result = pep8style.check_files(['models/amenity.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")


class test_inherit_basemodel(unittest.TestCase):
    """Test if user inherit from BaseModel"""

    def test_instance(self):
        """check if user is an instance of BaseModel"""
        user = Amenity()
        self.assertIsInstance(user, Amenity)
        self.assertTrue(issubclass(type(user), BaseModel))
        self.assertEqual(str(type(user)), "<class 'models.amenity.Amenity'>")


class test_Amenity_BaseModel(unittest.TestCase):
    """Testing user class"""

    def test_instances(self):
        with patch('models.amenity'):
            instance = Amenity()
            self.assertEqual(type(instance), Amenity)
            instance.name = "Barbie"
            expectec_attrs_types = {
                "id": str,
                "created_at": datetime,
                "updated_at": datetime,
                "name": str,
            }
            inst_dict = instance.to_dict()
            expected_dict_attrs = [
                "id",
                "created_at",
                "updated_at",
                "name",
                "__class__"
            ]
            self.assertCountEqual(inst_dict.keys(), expected_dict_attrs)
            self.assertEqual(inst_dict['name'], 'Barbie')
            self.assertEqual(inst_dict['__class__'], 'Amenity')

            for attr, types in expectec_attrs_types.items():
                with self.subTest(attr=attr, typ=types):
                    self.assertIn(attr, instance.__dict__)
                    self.assertIs(type(instance.__dict__[attr]), types)
            self.assertEqual(instance.name, "Barbie")

    def test_user_id_and_createat(self):
        """testing id for every user"""
        usr_1 = Amenity()
        sleep(2)
        usr_2 = Amenity()
        sleep(2)
        usr_3 = Amenity()
        sleep(2)
        list_usrs = [usr_1, usr_2, usr_3]
        for instance in list_usrs:
            usr_id = instance.id
            with self.subTest(user_id=usr_id):
                self.assertIs(type(usr_id), str)
        self.assertNotEqual(usr_1.id, usr_2.id)
        self.assertNotEqual(usr_1.id, usr_3.id)
        self.assertNotEqual(usr_2.id, usr_3.id)
        self.assertTrue(usr_1.created_at <= usr_2.created_at)
        self.assertTrue(usr_2.created_at <= usr_3.created_at)
        self.assertNotEqual(usr_1.created_at, usr_2.created_at)
        self.assertNotEqual(usr_1.created_at, usr_3.created_at)
        self.assertNotEqual(usr_3.created_at, usr_2.created_at)

    def test_str_method(self):
        """
        Testin str magic method
        """
        inst = Amenity()
        str_output = "[Amenity] ({}) {}".format(inst.id, inst.__dict__)
        self.assertEqual(str_output, str(inst))

    @patch('models.storage')
    def test_save_method(self, mock_storage):
        """Testing save method and if it update"""
        instance_5 = Amenity()
        created_at = instance_5.created_at
        sleep(2)
        updated_at = instance_5.updated_at
        instance_5.save()
        new_created_at = instance_5.created_at
        sleep(2)
        new_updated_at = instance_5.updated_at
        self.assertNotEqual(updated_at, new_updated_at)
        self.assertEqual(created_at, new_created_at)
        self.assertTrue(mock_storage.save.called)


class TestAmenity(unittest.TestCase):
    """Test the Amenity class"""

    def test_is_subclass(self):
        """Test that Amenity is a subclass of BaseModel"""
        amenity = Amenity()
        self.assertIsInstance(amenity, BaseModel)
        self.assertTrue(hasattr(amenity, "id"))
        self.assertTrue(hasattr(amenity, "created_at"))
        self.assertTrue(hasattr(amenity, "updated_at"))

    def test_name_attr(self):
        """Test that Amenity has attribute name, and it's as an empty string"""
        amenity = Amenity()
        self.assertTrue(hasattr(amenity, "name"))
        if storage_t == 'db':
            self.assertEqual(amenity.name, None)
        else:
            self.assertEqual(amenity.name, "")

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        amenity = Amenity()
        print(amenity.__dict__)
        new_d = amenity.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in amenity.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        amenity = Amenity()
        new_d = amenity.to_dict()
        self.assertEqual(new_d["__class__"], "Amenity")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"],
                         amenity.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"],
                         amenity.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        amenity = Amenity()
        string = "[Amenity] ({}) {}".format(amenity.id, amenity.__dict__)
        self.assertEqual(string, str(amenity))
