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
    """Tests for utils.get_json."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test utils.get_json with mocked requests.get using parameterized inputs."""
        with patch("utils.requests.get") as mock_get:
            mock_resp = Mock()
            mock_resp.json.return_value = test_payload
            mock_get.return_value = mock_resp

            result = get_json(test_url)
            self.assertEqual(result, test_payload)
            mock_get.assert_called_once_with(test_url)

if __name__ == "__main__":
    unittest.main()
