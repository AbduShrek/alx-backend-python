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

    def test_get_json(self):
        """Patch requests.get and verify payload + call count (no decorators)."""
        cases = [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
        for url, payload in cases:
            with self.subTest(url=url):
                with patch("utils.requests.get") as mock_get:
                    mock_resp = Mock()
                    mock_resp.json.return_value = payload
                    mock_get.return_value = mock_resp

                    # Assert return value
                    self.assertEqual(get_json(url), payload)
                    # Assert requests.get called exactly once with URL
                    mock_get.assert_called_once_with(url)

if __name__ == "__main__":
    unittest.main()
