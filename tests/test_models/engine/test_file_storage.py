import json
import os
import unittest
from unittest.mock import patch
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """testing the file storage class"""

    def setUp(self):
        self.storage = FileStorage()
        self.test_obj = BaseModel()
        self.storage.new(self.test_obj)

    def tearDown(self):
        self.storage._FileStorage__objects.clear()
        try:
            os.remove(FileStorage._FileStorage__file_path)
        except FileNotFoundError:
            pass

    def test_new(self):
        key = f"{self.test_obj.__class__.__name__}.{self.test_obj.id}"
        self.assertIn(key, self.storage._FileStorage__objects)

    def test_new_invalid_object(self):
        with self.assertRaises(AttributeError):
            self.storage.new(None)

    def test_save(self):
        self.storage.save()
        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))

    def test_reload(self):
        self.storage.save()
        self.storage._FileStorage__objects = {}
        self.storage.reload()
        key = f"{self.test_obj.__class__.__name__}.{self.test_obj.id}"
        self.assertIn(key, self.storage._FileStorage__objects)

    def test_reload_no_file(self):
        self.storage._FileStorage__objects = {}
        try:
            os.remove(FileStorage._FileStorage__file_path)
        except FileNotFoundError:
            pass
        self.storage.reload()
        self.assertEqual({}, self.storage._FileStorage__objects)

    def test_get_existing_object(self):
        obj = self.storage.get(BaseModel, self.test_obj.id)
        self.assertIsNotNone(obj)
        self.assertEqual(self.test_obj, obj)

    def test_get_existing_object_string(self):
        obj = self.storage.get("BaseModel", self.test_obj.id)
        self.assertIsNotNone(obj)
        self.assertEqual(self.test_obj, obj)

    def test_get_non_existing_class(self):
        obj = self.storage.get("NonExistentClass", "123")
        self.assertIsNone(obj)

    def test_get_non_existing_id(self):
        obj = self.storage.get(BaseModel, "123")
        self.assertIsNone(obj)

    def test_get_none_class(self):
        obj = self.storage.get(None, "123")
        self.assertIsNone(obj)

    def test_all(self):
        objs = self.storage.all()
        self.assertIsInstance(objs, dict)
        self.assertEqual(1, len(objs))

    def test_all_specific_cls(self):
        objs = self.storage.all(BaseModel)
        self.assertIsInstance(objs, dict)
        self.assertEqual(1, len(objs))

    def test_all_invalid_cls(self):
        objs = self.storage.all("NonExistentClass")
        self.assertIsNone(objs)

    def test_delete_existing_object(self):
        self.storage.delete(self.test_obj)
        key = f"{self.test_obj.__class__.__name__}.{self.test_obj.id}"
        self.assertNotIn(key, self.storage._FileStorage__objects)

    def test_delete_none_object(self):
        self.storage.delete(None)
        self.assertEqual(1, len(self.storage._FileStorage__objects))

    def test_close(self):
        with patch.object(self.storage, 'reload') as mock_reload:
            self.storage.close()
            mock_reload.assert_called_once()


if __name__ == '__main__':
    unittest.main()
