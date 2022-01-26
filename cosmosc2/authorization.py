#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
keycloak.py
"""

# Copyright 2022 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt

import time
import logging
import requests

from cosmosc2.__version__ import __title__
from cosmosc2.environment import *
from cosmosc2.decorators import request_wrapper, retry_wrapper

LOGGER = logging.getLogger(__title__)


def generate_auth():
    """
    Pick Auth class base on environment variables
    """
    if COSMOS_API_USER is None:
        return CosmosAuthorization()
    return CosmosKeycloakAuthorization()


class CosmosAuthorization(requests.auth.AuthBase):
    """Class to hold token for COSMOS

    The CosmosAuthorization can be used to call COSMOS server methods directly:
      auth = CosmosAuthorization()
      requests.get("example.org", auth=auth)
    """

    def get(self):
        return COSMOS_API_PASSWORD

    def __call__(self, r: requests.Request):
        r.headers["Authorization"] = COSMOS_API_PASSWORD
        return r

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def __str__(self):
        return f"<{self.__class__.__name__}>"


class CosmosKeycloakAuthorization(CosmosAuthorization):
    """Class to generate Keycloak token for COSMOS Enterprise
    https://developers.redhat.com/blog/2020/01/29/api-login-and-jwt-token-generation-using-keycloak

    The CosmosKeycloakAuthorization can be used to call the COSMOS keycloak server methods directly:
      auth = CosmosKeycloakAuthorization(schema="", hostname="127.0.0.1", port=7777)
      requests.get("example.org", auth=auth)
    """

    def __init__(
        self,
        schema: str = COSMOS_API_SCHEMA,
        hostname: str = COSMOS_API_HOSTNAME,
        port: int = COSMOS_API_PORT,
    ):
        """Constructor

        Parameters:
        schema -- The schema to connect to cosmos with
        hostname -- The name of the machine which has started the JSON service
        port -- The port number of the JSON service
        """
        self.request_url = f"{schema}://{hostname}:{port}"
        self.refresh_token = None
        self.expires_at = None
        self.refresh_expires_at = None
        self.token = None
    
    def _time_logic(self):
        current_time = time.time()
        if self.token is None:
            self._make_token()
        elif self.refresh_expires_at < current_time:
            self._make_token()
        elif self.expires_at < current_time:
            self._refresh_token()

    def get(self):
        self._time_logic()
        return f"Bearer {self.token}"

    def __call__(self, r: requests.Request):
        self._time_logic()
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r

    def _make_token(self):
        """
        {
            "access_token": "",
            "expires_in": 600,
            "refresh_expires_in": 1800,
            "refresh_token": "",
            "token_type": "bearer",
            "id_token": "",
            "not-before-policy": 0,
            "session_state": "",
            "scope": "openid email profile"
        }
        """
        oath = self._make_token_request().json()
        self.token = oath["access_token"]
        self.refresh_token = oath["refresh_token"]
        current_time = time.time()
        self.expires_at = current_time + oath["expires_in"]
        self.refresh_expires_at = current_time + oath["refresh_expires_in"]

    @request_wrapper
    @retry_wrapper
    def _make_token_request(self):
        """Use the python requests libary to request a token from Cosmos Keycloak.

        This is an internal method that uses two decorators. request_wrapper
        captures errors from the request libary. retry_wrapper captures exceptions
        from the requst_wrapper and will retry or bubble up the error.
        return -- request.Response
            https://docs.python-requests.org/en/master/user/quickstart/#json-response-content
        """
        request_kwargs = {
            "url": f"{self.request_url}/auth/realms/COSMOS/protocol/openid-connect/token",
            "data": f"username={COSMOS_API_USER}&password={COSMOS_API_PASSWORD}&client_id={COSMOS_API_CLIENT}&grant_type=password&scope=openid",
            "headers": {
                "User-Agent": USER_AGENT,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        }
        LOGGER.debug("calling with %s", request_kwargs)
        resp = requests.post(**request_kwargs)
        LOGGER.debug(
            "resp: %s total_seconds: %f content: %s",
            resp,
            resp.elapsed.total_seconds(),
            resp.content,
        )
        return resp

    def _refresh_token(self):
        """
        {
            "access_token": "",
            "expires_in": 600,
            "refresh_expires_in": 1800,
            "refresh_token": "",
            "token_type": "bearer",
            "id_token": "",
            "not-before-policy": 0,
            "session_state": "",
            "scope": "openid email profile"
        }
        """
        oath = self._make_refresh_request().json()
        self.token = oath["access_token"]
        self.refresh_token = oath["refresh_token"]
        current_time = time.time()
        self.expires_at = current_time + oath["expires_in"]
        self.refresh_expires_at = current_time + oath["refresh_expires_in"]

    @request_wrapper
    @retry_wrapper
    def _make_refresh_request(self):
        """Use the python requests libary to refresh the token.

        This is an internal method that uses two decorators. request_wrapper
        captures errors from the request libary. retry_wrapper captures exceptions
        from the requst_wrapper and will retry or bubble up the error.
        return -- request.Response
            https://docs.python-requests.org/en/master/user/quickstart/#json-response-content
        """
        request_kwargs = {
            "url": f"{self.request_url}/auth/realms/COSMOS/protocol/openid-connect/token",
            "data": f"client_id={COSMOS_API_CLIENT}&grant_type=refresh_token&refresh_token={self.refresh_token}",
            "headers": {
                "User-Agent": USER_AGENT,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        }
        LOGGER.debug("calling with %s", request_kwargs)
        resp = requests.post(**request_kwargs)
        LOGGER.debug(
            "resp: %s total_seconds: %f content: %s",
            resp,
            resp.elapsed.total_seconds(),
            resp.content,
        )
        return resp
