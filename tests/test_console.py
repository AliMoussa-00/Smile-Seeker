#!/usr/bin/env python3
"""testing the console module"""
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models.base_model import BaseModel


class TestHBNBCommand(unittest.TestCase):
    """unittest class of console"""
    def setUp(self):
        self.cli = HBNBCommand()

    @patch('sys.stdout', new_callable=StringIO)
    def assert_stdout(self, expected_output, mock_stdout, function=None, args=None):
        if function:
            function(args)
        output = mock_stdout.getvalue()
        self.assertEqual(output.strip(), expected_output)

    def test_default_not_found(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.assertFalse(self.cli.default("unknown.command"))
            self.assertIn("*** Unknown syntax: unknown.command", mock_stdout.getvalue())

    def test_create_without_class_name(self):
        self.assert_stdout("** class name missing **", function=self.cli.do_create, args="")

    def test_create_with_invalid_class(self):
        self.assert_stdout("** invalid class name **", function=self.cli.do_create, args="FakeClass")

    @patch('models.storage')
    def test_create_with_valid_class(self, mock_storage):
        BaseModel_instance = BaseModel()
        mock_storage.new.return_value = None
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.do_create("BaseModel")
            self.assertRegex(mock_stdout.getvalue(), r"\b\w{8}-\w{4}-\w{4}-\w{4}-\w{12}\b")

    def test_parse_params_empty(self):
        self.assertIsNone(self.cli.parse_params(""))

    def test_parse_params_single(self):
        self.assertEqual(self.cli.parse_params("key=value"), {"key": "value"})

    def test_parse_params_multiple(self):
        # params is a string delimited by "="
        self.assertEqual(self.cli.parse_params("name=John Doe=age=30"), {"name": "John Doe", "age": 30})

    def test_do_all_with_invalid_class(self):
        self.assert_stdout("** invalid class name **", function=self.cli.do_all, args="FakeClass")

    @patch('models.storage')
    def test_do_all_with_valid_class(self, mock_storage):
        mock_storage.all.return_value = {}
        self.assert_stdout("{}", function=self.cli.do_all, args="BaseModel")

    def test_do_update_missing_class_name(self):
        self.assert_stdout("** class name is missing **", function=self.cli.do_update, args="")

    def test_do_update_invalid_class_name(self):
        self.assert_stdout("** invalid class name **", function=self.cli.do_update, args="FakeClass 123")

    def test_do_update_missing_id(self):
        self.assert_stdout("** id is missing **", function=self.cli.do_update, args="BaseModel")

    @patch('models.storage')
    def test_do_update_invalid_id(self, mock_storage):
        mock_storage.get.return_value = None
        self.assert_stdout("** invalid instance id **", function=self.cli.do_update, args="BaseModel 123")

    @patch('models.storage')
    def test_do_update_missing_key(self, mock_storage):
        self.assert_stdout("** key is missing **", function=self.cli.do_update, args="BaseModel 123")

    @patch('models.storage')
    def test_do_update_missing_value(self, mock_storage):
        self.assert_stdout("** value is missing **", function=self.cli.do_update, args="BaseModel 123 key")

    def test_do_delete_missing_class_name(self):
        self.assert_stdout("** class name is missing **", function=self.cli.do_delete, args="")

    def test_do_delete_invalid_class_name(self):
        self.assert_stdout("** invalid class name **", function=self.cli.do_delete, args="FakeClass 123")

    @patch('models.storage')
    def test_do_delete_missing_id(self, mock_storage):
        self.assert_stdout("** id is missing **", function=self.cli.do_delete, args="BaseModel")

    @patch('models.storage')
    def test_do_delete_invalid_id(self, mock_storage):
        mock_storage.get.return_value = None
        self.assert_stdout("** invalid instance id **", function=self.cli.do_delete, args="BaseModel 123")

    def test_do_count_missing_class_name(self):
        self.assert_stdout("** class name is missing **", function=self.cli.do_count, args="")

    def test_do_count_invalid_class_name(self):
        self.assert_stdout("** invalid class name **", function=self.cli.do_count, args="FakeClass")

    @patch('models.storage')
    def test_do_count_valid_class_name(self, mock_storage):
        mock_storage.all.return_value = {}
        self.assert_stdout("0", function=self.cli.do_count, args="BaseModel")


if __name__ == '__main__':
    unittest.main()
