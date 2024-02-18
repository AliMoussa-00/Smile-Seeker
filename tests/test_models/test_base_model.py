"""testing the base_model"""
from models.base_model import BaseModel
from datetime import datetime, timedelta
import unittest
import uuid


class TestBaseModel(unittest.TestCase):
    """testing the BaseModel class"""
    def setUp(self):
        # Run before every test
        pass

    def test_instance_creation(self):
        # Test regular creation of an instance
        instance = BaseModel()
        self.assertIsInstance(instance, BaseModel)
        self.assertTrue(hasattr(instance, 'id'))
        self.assertTrue(hasattr(instance, 'created_at'))
        self.assertTrue(hasattr(instance, 'updated_at'))

    def test_uuid_generation(self):
        # Test if id is a valid uuid
        instance = BaseModel()
        try:
            uuid.UUID(str(instance.id), version=4)
        except ValueError:
            self.fail("id is not a valid uuid4")

    def test_datetime_assignment(self):
        # Test if created_at and updated_at are valid datetimes
        instance = BaseModel()
        self.assertIsInstance(instance.created_at, datetime)
        self.assertIsInstance(instance.updated_at, datetime)

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


if __name__ == "__main__":
    unittest.main()
