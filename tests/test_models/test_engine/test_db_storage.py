#!/usr/bin/python3
"""testing db storage modeul"""

import unittest
from unittest.mock import MagicMock
from models.users import Users
from sqlalchemy.orm import scoped_session
from models.engine.db_storage import DBStorage  # Replace with your actual file name

import models


class TestDBStorage(unittest.TestCase):
    """defining the db storage test class"""

    @unittest.skipIf(models.storage_type != 'db', "not testing db storage")
    def setUp(self):
        self.storage = DBStorage()
        self.storage.reload()

    @unittest.skipIf(models.storage_type != 'db', "not testing db storage")
    def test_init(self):
        self.assertTrue(hasattr(self.storage, "_DBStorage__engine"))
        self.assertTrue(hasattr(self.storage, "_DBStorage__session"))

    @unittest.skipIf(models.storage_type != 'db', "not testing db storage")
    def test_reload(self):
        self.storage._DBStorage__engine = MagicMock()
        self.storage.reload()
        self.assertIsNotNone(self.storage._DBStorage__session)

    @unittest.skipIf(models.storage_type != 'db', "not testing db storage")
    def test_all_with_no_class(self):
        session = self.storage._DBStorage__session = MagicMock()
        session.query().all.return_value = []
        objs = self.storage.all()
        self.assertIsInstance(objs, dict)
        self.assertEqual(len(objs), 0)

    @unittest.skipIf(models.storage_type != 'db', "not testing db storage")
    def test_all_with_valid_class(self):
        session = self.storage._DBStorage__session = MagicMock()
        session.query().all.return_value = []
        objs = self.storage.all(cls="Users")
        self.assertIsInstance(objs, dict)
        self.assertEqual(len(objs), 0)

    @unittest.skipIf(models.storage_type != 'db', "not testing db storage")
    def test_all_with_invalid_class(self):
        objs = self.storage.all(cls="NonExistentClass")
        self.assertIsInstance(objs, dict)
        self.assertEqual(len(objs), 0)

    @unittest.skipIf(models.storage_type != 'db', "not testing db storage")
    def test_new_with_valid_obj(self):
        obj = Users()
        session = self.storage._DBStorage__session = MagicMock()
        self.storage.new(obj=obj)
        session.add.assert_called_once_with(obj)

    @unittest.skipIf(models.storage_type != 'db', "not testing db storage")
    def test_new_with_none_obj(self):
        session = self.storage._DBStorage__session = MagicMock()
        self.storage.new(obj=None)
        session.add.assert_not_called()

    @unittest.skipIf(models.storage_type != 'db', "not testing db storage")
    def test_save(self):
        session = self.storage._DBStorage__session = MagicMock()
        self.storage.save()
        session.commit.assert_called_once()

    @unittest.skipIf(models.storage_type != 'db', "not testing db storage")
    def test_get_with_valid_args(self):
        fake_user = Users()
        fake_user.id = "12345"
        session = self.storage._DBStorage__session = MagicMock()
        session.query().all.return_value = [fake_user]
        user = self.storage.get(Users, "12345")
        self.assertEqual(user, fake_user)

    @unittest.skipIf(models.storage_type != 'db', "not testing db storage")
    def test_get_with_invalid_id(self):
        user = self.storage.get(Users, "nonexistent")
        self.assertIsNone(user)

    @unittest.skipIf(models.storage_type != 'db', "not testing db storage")
    def test_get_with_invalid_class(self):
        user = self.storage.get("NonExistentClass", "12345")
        self.assertIsNone(user)

    @unittest.skipIf(models.storage_type != 'db', "not testing db storage")
    def test_delete_with_valid_obj(self):
        obj = Users()
        session = self.storage._DBStorage__session = MagicMock()
        self.storage.delete(obj)
        session.delete.assert_called_once_with(obj)

    def test_delete_with_none_obj(self):
        session = self.storage._DBStorage__session = MagicMock()
        self.storage.delete(None)
        session.delete.assert_not_called()

    @unittest.skipIf(models.storage_type != 'db', "not testing db storage")
    def test_close(self):
        session = self.storage._DBStorage__session = MagicMock(spec=scoped_session)
        self.storage.close()
        session.remove.assert_called_once()


if __name__ == "__main__":
    # !! please use the file 'test_db_storage' to test this file
    # because it needs environment variables
    unittest.main()
