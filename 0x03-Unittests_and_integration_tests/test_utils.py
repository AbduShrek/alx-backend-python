#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map
from unittest.mock import patch, Mock
from utils import memoize

"""
Unit tests for utils.py functions and decorators.

This module contains tests for:
- access_nested_map (Task 0 & 1)
- get_json (Task 2)
- memoize (Task 3)
"""


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
    """Unit tests for utils.get_json."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Patch requests.get and verify single call + returned payload."""
        with patch("utils.requests.get") as mock_get:
            mock_resp = Mock()
            mock_resp.json.return_value = test_payload
            mock_get.return_value = mock_resp

            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Unit tests for utils.memoize decorator."""

    def test_memoize(self):
        """
        Test that a_method is only called once even when
        a_property is accessed multiple times.
        """

        class TestClass:
            """Helper class to test memoize decorator."""

            def a_method(self):
                """Return a fixed number (42)."""
                return 42

            @memoize
            def a_property(self):
                """Return a_method result, memoized by decorator."""
                return self.a_method()

        obj = TestClass()
        with patch.object(TestClass, "a_method",
                          return_value=42) as mock_method:
            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
