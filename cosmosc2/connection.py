#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
connection.py
"""

# Copyright 2021 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt

import json
import logging
from requests import Session
from threading import RLock, Event
from contextlib import ContextDecorator

from cosmosc2.__version__ import __title__
from cosmosc2.environment import *
from cosmosc2.exceptions import CosmosConnectionError
from cosmosc2.decorators import request_wrapper, retry_wrapper
from cosmosc2.json_rpc import JsonRpcRequest, JsonRpcResponse

LOGGER = logging.getLogger(__title__)


class Connection(ContextDecorator):
    """Class to perform JSON-RPC Calls to the COSMOS Server (or other JsonDrb server)

    The Connection can be used to call COSMOS server methods directly:
      server = Connection(hostname: "127.0.0.1", port: 7777)
      server.write(...)
    """

    def __init__(
        self,
        schema: str = COSMOS_SCHEMA,
        hostname: str = COSMOS_HOSTNAME,
        port: int = COSMOS_PORT,
        timeout: float = 5.0,
        scope: str = COSMOS_SCOPE,
    ):
        """Constructor

        Parameters:
        hostname -- The name of the machine which has started the JSON service
        port -- The port number of the JSON service
        timeout -- The amount of time the socket will read until an error
        scope -- The scope or project the connection will add to the request
        """
        self.id = 0
        self.scope = scope
        self.timeout = float(timeout)
        self.url = "{}://{}:{}".format(schema, hostname, port)
        self._session = Session()
        self._session.headers = {
            "User-Agent": USER_AGENT,
            "Authorization": COSMOS_TOKEN,
        }
        self._mutex = RLock()
        self._shutdown_needed = Event()

    def shutdown(self):
        """Permanently disconnects from the JSON server"""
        self._shutdown_needed.set()
        self._session.close()

    def json_rpc_request(self, method_name, *args, **kwargs):
        """Forwards all method calls to the remote service.

        method_name -- Name of the method to call
        args -- Array of parameters to pass to the method
        kwargs -- Dict of parameters to pass to the method
        return -- The result of the method call. If something goes wrong with the
          protocol a exception extended from RuntimeError is raised.
        """
        if self._shutdown_needed.is_set():
            raise CosmosConnectionError("shutdown event is set, exiting")
        with self._mutex:
            self.id += 1
            json_rpc_request = JsonRpcRequest(
                self.id, method_name, self.scope, *args, **kwargs
            )
            resp = self._make_json_rpc_request(json_rpc_request.to_hash())
            try:
                json_rpc_response = JsonRpcResponse.from_bytes(resp.content)
                LOGGER.debug("response %s %s", type(json_rpc_response), json_rpc_response)
                return json_rpc_response.result
            except AttributeError:
                return json_rpc_response

    @request_wrapper
    @retry_wrapper
    def _make_json_rpc_request(self, hash_: dict):
        """Use the python requests libary to send the request to Cosmos.

        This is an internal method that uses two decorators. request_wrapper
        captures errors from the request libary. retry_wrapper captures exceptions
        from the requst_wrapper and will retry or bubble up the error.
        return -- bytes: request.content
            https://docs.python-requests.org/en/master/user/quickstart/#binary-response-content
        """
        request_kwargs = {
            "url": "{}/cosmos-api/api".format(self.url),
            "data": json.dumps(hash_),
            "headers": {
                "Content-Type": "application/json-rpc",
            },
        }
        LOGGER.debug("calling with %s", request_kwargs)
        resp = self._session.post(**request_kwargs)
        LOGGER.debug(
            "resp: %s total_seconds: %f content: %s",
            resp,
            resp.elapsed.total_seconds(),
            resp.content,
        )
        return resp
