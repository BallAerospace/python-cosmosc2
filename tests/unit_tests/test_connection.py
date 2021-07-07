#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
test_drb_object.py
"""

import os
import unittest
from unittest.mock import patch, MagicMock

from cosmosc2.connection import Connection


class TestConnection(unittest.TestCase):

    HOST, PORT = "127.0.0.1", 7777

    @patch("cosmosc2.connection.Session.post")
    def test_object(self, post):
        """
        Test json request
        """
        connection = Connection(hostname=self.HOST, port=self.PORT)
        post.assert_not_called()
        self.assertIsNotNone(connection._session)
        self.assertIsNotNone(connection.url)
        self.assertTrue(self.HOST in connection.url)
        self.assertTrue(str(self.PORT) in connection.url)

    @patch("cosmosc2.connection.Session.post")
    def test_object_localhost(self, post):
        """
        Test json request
        """
        connection = Connection()
        post.assert_not_called()
        self.assertIsNotNone(connection._session)
        self.assertIsNotNone(connection.url)
        self.assertTrue(self.HOST in connection.url)
        self.assertTrue("2900" in connection.url)

    @patch("cosmosc2.connection.Session.post")
    def test_object_tacocat(self, post):
        """
        Test json request
        """
        hostname = "tacocat"
        connection = Connection(hostname=hostname, port=self.PORT)
        post.assert_not_called()
        self.assertIsNotNone(connection._session)
        self.assertIsNotNone(connection.url)
        self.assertTrue(hostname in connection.url)
        self.assertTrue(str(self.PORT) in connection.url)

    @patch("cosmosc2.connection.Session.post")
    def test_connection(self, post):
        """
        Test connection
        """
        ret = b'{"jsonrpc": "2.0", "id": 107, "result": 0}'
        post.return_value = MagicMock(status_code=200, content=ret)
        connection = Connection()
        connection.json_rpc_request(self.test_connection.__name__)
        self.assertIsNotNone(connection._session)
        post.assert_called_once()

    @patch("cosmosc2.decorators.time.sleep")
    @patch("cosmosc2.connection.Session.post")
    def test_connection_refused_error(self, post, sleep):
        """
        Test connection
        """
        sleep.return_value = None
        post.return_value = MagicMock(side_effect=ConnectionRefusedError("test"))
        connection = Connection()
        with self.assertRaises(RuntimeError):
            connection.json_rpc_request(self.test_connection_refused_error.__name__)
        self.assertIsNotNone(connection._session)
        post.assert_called_once()

    @patch("cosmosc2.connection.Session.post")
    def test_connection_error(self, post):
        """
        Test connection
        """
        post.return_value = MagicMock(side_effect=ConnectionError("test"))
        connection = Connection()
        with self.assertRaises(RuntimeError):
            connection.json_rpc_request(self.test_connection_error.__name__)
        self.assertIsNotNone(connection._session)
        post.assert_called_once()

    @patch("cosmosc2.connection.Session.post")
    def test_response_timeout_error(self, post):
        """
        Test connection
        """
        from requests import Timeout

        post.return_value = MagicMock(side_effect=Timeout("test"))
        connection = Connection()
        with self.assertRaises(RuntimeError):
            connection.json_rpc_request(self.test_response_timeout_error.__name__)
        self.assertIsNotNone(connection._session)
        post.assert_called()

    @patch("cosmosc2.connection.Session.post")
    def test_response_none(self, post):
        """
        Test connection
        """
        post.return_value = MagicMock(content=None)
        connection = Connection()
        with self.assertRaises(RuntimeError):
            connection.json_rpc_request(self.test_response_none.__name__)
        self.assertIsNotNone(connection._session)
        print(post)
        post.assert_called_once()

    @patch("cosmosc2.connection.Session.post")
    def test_response_status_code(self, post):
        """
        Test connection
        """
        post.return_value = MagicMock(status_code=500)
        connection = Connection()
        with self.assertRaises(RuntimeError):
            connection.json_rpc_request(self.test_response_none.__name__)
        self.assertIsNotNone(connection._session)
        post.assert_called()

    @patch("cosmosc2.connection.Session.post")
    def test_response_error(self, post):
        """
        Test connection
        """
        post.return_value = MagicMock(side_effect=ConnectionResetError("test"))
        connection = Connection()
        with self.assertRaises(RuntimeError):
            connection.json_rpc_request(self.test_response_error.__name__)
        self.assertIsNotNone(connection._session)
        post.assert_called_once()

    @patch("cosmosc2.connection.Session.post")
    def test_response_result_error(self, post):
        """
        Test connection
        """
        ret = b"""
            {
                "jsonrpc": "2.0",
                "id": 107,
                "error": {
                    "code": "1234",
                    "message": "foobar",
                    "data": {
                        "foo": "bar"
                    }
                }
            }
        """
        post.return_value = MagicMock(content=ret)
        connection = Connection()
        response = connection.json_rpc_request(self.test_response_result_error.__name__)
        self.assertIsNotNone(response)
        post.assert_called_once()

    @patch("cosmosc2.connection.Session.post")
    def test_response_result_invalid(self, post):
        """
        Test connection
        """
        ret = b'{"jsonrpc": "2.0", "id": 107}'
        post.return_value = MagicMock(content=ret)
        connection = Connection()
        with self.assertRaises(RuntimeError):
            connection.json_rpc_request(self.test_response_result_invalid.__name__)
        self.assertIsNotNone(connection._session)
        post.assert_called_once()


if __name__ == "__main__":
    unittest.main()
