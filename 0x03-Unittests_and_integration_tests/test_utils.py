#!/usr/bin/env python3
"""class that inherits from unittest"""
import unittest
from parameterized import parameterized
from utils import access_nested_map
from utils import get_json, memoize
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """class for testing access_nestd_map function"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{path[-1]}'")


class TestGetJson(unittest.TestCase):
    """method to test that utils.get_json returns the expected"""
    @patch("utils.requests.get")
    def test_get_json(self, mock_get):
        """class and implement the TestGetJson.test_get_json"""
        test_cases = [
            {"test_url": "http://example.com", "test_payload": {
                "payload": True}},
            {"test_url": "http://holberton.io", "test_payload": {
                "payload": False}},
        ]
        for case in test_cases:
            test_url = case["test_url"]
            test_payload = case["test_payload"]
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)
            mock_get.reset_mock()


class TestMemoize(unittest.TestCase):
    """test class to test memoize"""
    def test_memoize(self):
        """
        Tests the function when calling a_property twice,
        the correct result is returned but a_method is only
        called once using assert_called_once
       """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()
        obj = TestClass()
        with patch.object(obj, 'a_method', return_value=42) as mock_method:
            result_first_call = obj.a_property
            result_second_call = obj.a_property
            self.assertEqual(result_first_call, 42)
            self.assertEqual(result_second_call, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
