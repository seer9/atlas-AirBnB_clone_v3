#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""
import unittest
import os
from models import storage
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
import inspect
import pep8

FileStorage = FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    def setUp(self):
        """Set up for the tests"""
        self.storage = FileStorage()
        self.storage.reload()

    def tearDown(self):
        """Tear down after the tests"""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_all_return_type(self):
        """Test that all returns a dictionary"""
        self.assertIsInstance(self.storage.all(), dict)

    def test_new_method(self):
        """Test the new method"""
        obj = BaseModel()
        self.storage.new(obj)
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.assertIn(key, self.storage.all())

    def test_objects_value_type(self):
        """Test that the values in __objects are instances of BaseModel"""
        obj = BaseModel()
        self.storage.new(obj)
        self.assertIsInstance(list(self.storage.all().values())[0], BaseModel)

    def test_save_file_exists(self):
        """Test that save creates a file"""
        self.storage.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_save_file_read(self):
        """Test that save writes to the file"""
        self.storage.save()
        with open("file.json", "r") as f:
            content = f.read()
        self.assertIn("BaseModel", content)

    def test_the_type_file_content(self):
        """Test the type of the content in the file"""
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        with open("file.json", "r") as f:
            content = f.read()
        self.assertIsInstance(content, str)

    def test_reload_without_file(self):
        """Test reload without a file"""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        self.storage.reload()
        self.assertEqual(self.storage.all(), {})

    def test_delete(self):
        """Test the delete method"""
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        self.storage.delete(obj)
        self.assertNotIn(obj, self.storage.all().values())

    def test_model_storage(self):
        """Test that the model is stored correctly"""
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        self.assertIn(obj, self.storage.all().values())

    def test_get(self):
        """Test the get method"""
        obj = BaseModel()
        obj_id = obj.id
        self.storage.new(obj)
        self.storage.save()
        self.assertEqual(self.storage.get(BaseModel, obj_id), obj)
        self.assertIsNone(self.storage.get(BaseModel, "nonexistent_id"))

    def test_count(self):
        """Test the count method"""
        initial_count = self.storage.count()
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        self.assertEqual(self.storage.count(), initial_count + 1)
        self.assertEqual(self.storage.count(BaseModel), initial_count + 1)


if __name__ == "__main__":
    unittest.main()


