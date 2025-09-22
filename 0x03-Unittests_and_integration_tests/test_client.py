#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient.org."""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient.org property."""

    @patch("client.get_json")
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    def test_org(self, org_name, mock_get_json):
        """
        Ensure .org calls get_json once with the right URL and returns
        the mocked payload.
        """
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected_payload)

        mock_get_json.assert_called_once_with(
            GithubOrgClient.ORG_URL.format(org=org_name)
        )


        def test_public_repos_url(self):
        """_public_repos_url returns repos_url from the mocked org payload."""
        payload = {"repos_url": "https://api.github.com/orgs/google/repos"}
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, payload["repos_url"])

        def test_public_repos(self):
                """
                public_repos returns repo names and calls get_json
                with the _public_repos_url value exactly once.
                """
                repos_payload = [
                    {"name": "alpha"},
                    {"name": "beta"},
                    {"name": "gamma"},
                ]
                fake_url = "https://api.github.com/orgs/google/repos"
        
                with patch.object(
                    GithubOrgClient, "_public_repos_url",
                    new_callable=PropertyMock, return_value=fake_url
                ) as mock_url, patch(
                    "client.get_json"
                ) as mock_get_json:
                    mock_get_json.return_value = repos_payload
        
                    client = GithubOrgClient("google")
                    self.assertEqual(client.public_repos(), ["alpha", "beta", "gamma"])
        
                    mock_url.assert_called_once()
                    mock_get_json.assert_called_once_with(fake_url)
        
            # --- Task 6: More patching (with license filter) ---
            @parameterized.expand([
                ("apache-2.0", [
                    {"name": "alpha", "license": {"key": "apache-2.0"}},
                    {"name": "beta", "license": {"key": "bsd-3-clause"}},
                    {"name": "gamma", "license": {"key": "apache-2.0"}},
                ], ["alpha", "gamma"]),
                ("bsd-3-clause", [
                    {"name": "alpha", "license": {"key": "apache-2.0"}},
                    {"name": "beta", "license": {"key": "bsd-3-clause"}},
                ], ["beta"]),
            ])
            def test_public_repos_with_license(self, license_key, payload, expected):
                """
                public_repos filters by license using has_license,
                returning only names matching the license.
                """
                fake_url = "https://api.github.com/orgs/google/repos"
        
                with patch.object(
                    GithubOrgClient, "_public_repos_url",
                    new_callable=PropertyMock, return_value=fake_url
                ) as mock_url, patch(
                    "client.get_json"
                ) as mock_get_json:
                    mock_get_json.return_value = payload
        
                    client = GithubOrgClient("google")
                    self.assertEqual(client.public_repos(license=license_key), expected)
        
                    mock_url.assert_called_once()
                    mock_get_json.assert_called_once_with(fake_url)


if __name__ == "__main__":
    unittest.main()
