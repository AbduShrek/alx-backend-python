#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map
from unittest.mock import patch, Mock

class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for utils.access_nested_map."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns the correct value."""
        self.assertEqual(access_nested_map(nested_map, path), expected)
        
    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, missing_key):
        """Test that KeyError is raised with the missing key in message."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(cm.exception.args[0], missing_key)

class TestGetJson(unittest.TestCase):
    """Unit tests for utils.get_json"""

    def test_get_json(self):
       """Test the get_json function"""
        test_cases = [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]

        for test_url, test_payload in test_cases:
            with self.subTest(url=test_url, payload=test_payload):
                with patch('utils.requests.get') as mock_get:
                    mock_response = Mock()
                    mock_response.json.return_value = test_payload
                    mock_get.return_value = mock_response

                    result = get_json(test_url)

                    mock_get.assert_called_once_with(test_url)
                    self.assertEqual(result, test_payload)

if __name__ == "__main__":
    unittest.main()
