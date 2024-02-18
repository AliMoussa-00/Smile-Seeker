"""testing the base_model"""
from unittest.mock import patch

from models.base_model import BaseModel
from datetime import datetime, timedelta

import models
import unittest


class TestBaseModel(unittest.TestCase):
    """testing the BaseModel class"""
    def setUp(self):
        # Run before every test
        pass

    def test_init_no_kwargs(self):
        """Test BaseModel initialization without kwargs"""
        b = BaseModel()
        self.assertIsNotNone(b.id)
        self.assertTrue(isinstance(b.id, str))
        self.assertTrue(isinstance(b.created_at, datetime))
        self.assertTrue(isinstance(b.updated_at, datetime))

    def test_init_with_kwargs(self):
        """Test BaseModel initialization with kwargs"""
        kw = {'name': 'test', 'number': 42}
        b = BaseModel(**kw)
        self.assertEqual(b.name, 'test')
        self.assertEqual(b.number, 42)

    @patch('models.base_model.uuid.uuid4')
    def test_init_id(self, mock_uuid):
        """Test BaseModel id is a UUID4"""
        mock_uuid.return_value = '1234'
        b = BaseModel()
        self.assertEqual(b.id, '1234')

    def test_dates_are_datetime(self):
        """Test created_at and updated_at are datetime instances"""
        b = BaseModel()
        self.assertTrue(isinstance(b.created_at, datetime))
        self.assertTrue(isinstance(b.updated_at, datetime))

    def test_string_representation(self):
        # Test string representation
        instance = BaseModel()
        expected_str = f"[BaseModel] ({instance.id}) {instance.__dict__}"
        self.assertEqual(str(instance), expected_str)

    def test_to_dict(self):
        # Test to_dict method
        instance = BaseModel()
        instance_dict = instance.to_dict()

        self.assertEqual(instance_dict["__class__"], "BaseModel")
        self.assertIsInstance(instance_dict["created_at"], str)
        self.assertIsInstance(instance_dict["updated_at"], str)

        # Check if isoformat is correct
        try:
            datetime.fromisoformat(instance_dict['created_at'])
            datetime.fromisoformat(instance_dict['updated_at'])
        except ValueError:
            self.fail("created_at or updated_at are not in isoformat")

    def test_datetime_initialization_from_kwargs(self):
        # Test creation with provided datetime as strings in kwargs
        created_at = datetime.now() - timedelta(days=1)
        updated_at = datetime.now()

        instance = BaseModel(created_at=created_at.isoformat(), updated_at=updated_at.isoformat())

        self.assertEqual(instance.created_at, created_at)
        self.assertEqual(instance.updated_at, updated_at)

    def test_kwargs_attributes_assignment(self):
        # Test if additional kwargs are correctly assigned as instance attributes
        kwargs = {'name': 'test_name', 'value': 42}
        instance = BaseModel(**kwargs)

        for key, value in kwargs.items():
            self.assertTrue(hasattr(instance, key))
            self.assertEqual(getattr(instance, key), value)

    def test_excluding_class_kwarg(self):
        # Test if the '__class__' kwarg is not assigned as an instance attribute
        instance = BaseModel(__class__='This should not be an attribute')

        self.assertNotEqual(instance.__class__.__name__, 'This should not be an attribute')

    def test_invalid_datetime_strings(self):
        # Test with invalid datetime strings, should not raise error, but not change the dates
        with self.assertRaises(ValueError):
            BaseModel(created_at='invalid datetime', updated_at='another invalid datetime')

    def test_update_timestamps(self):
        """Test save method updates the updated_at timestamp"""
        b = BaseModel()
        first_updated_at = b.updated_at
        with patch('base_model.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime.now() + timedelta(seconds=10)
            b.save()
        self.assertNotEqual(first_updated_at, b.updated_at)

    def test_update_with_kwargs(self):
        """Test update method with kwargs"""
        b = BaseModel()
        initial_updated_at = b.updated_at
        b.update(name='new_name')
        self.assertEqual(b.name, 'new_name')
        self.assertNotEqual(initial_updated_at, b.updated_at)

    def test_update_ignore_protected_attrs(self):
        """Test update method ignores id, created_at and updated_at"""
        b = BaseModel()
        initial_id = b.id
        initial_created_at = b.created_at
        initial_updated_at = b.updated_at
        b.update(id='new_id', created_at=datetime.now(), updated_at=datetime.now())
        self.assertEqual(initial_id, b.id)
        self.assertEqual(initial_created_at, b.created_at)
        self.assertEqual(initial_updated_at, b.updated_at)

    def test_delete(self):
        """Test delete method"""
        b = BaseModel()
        b.delete()
        models.storage.delete.assert_called_with(b)

    def test_save_new_object(self):
        """Test save method adds new object to storage"""
        b = BaseModel()
        b.save()
        models.storage.new.assert_called_with(b)
        models.storage.save.assert_called()

    def test_save_existing_object(self):
        """Test save method updates existing object in storage"""
        b = BaseModel()
        models.storage.get.return_value = b
        b.save()
        models.storage.new.assert_not_called()
        models.storage.save.assert_called()


if __name__ == "__main__":
    unittest.main()
