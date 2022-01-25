#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
stream.py
"""

# Copyright 2022 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt

import asyncio
import json
import logging
from threading import Thread
import websockets

from cosmosc2.environment import *

logger = logging.getLogger("websockets")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

class CosmosAsyncError(RuntimeError):
    pass

class CosmosAsyncStop(StopAsyncIteration):
    pass

class CosmosAsyncStream(Thread):
    def __init__(
        self,
        schema: str = COSMOS_WS_SCHEMA,
        hostname: str = COSMOS_API_HOSTNAME,
        port: int = COSMOS_API_PORT,
    ):
        super().__init__()
        self._tasks = {}
        self._events = {}
        self._queues = {}
        self._loop = asyncio.new_event_loop()
        self._stop_event = asyncio.Event(loop=self._loop)
        self._url = f"{schema}://{hostname}:{port}"

    def run(self):
        try:
            self._loop.run_until_complete(self._stop_event.wait())
            self._loop.run_until_complete(self._clean())
        finally:
            self._loop.close()

    def stop(self):
        try:
            self._loop.call_soon_threadsafe(self._stop_event.set)
        except Exception:
            pass

    async def _clean(self):
        for endpoint, task in self._tasks.items():
            logging.info(f"canceling endpoint {endpoint}")
            task.cancel()
        await asyncio.gather(*self._tasks.values(), loop=self._loop)

    def subscribe(self, endpoint, sub_msg, callback):
        def _subscribe():
            if endpoint not in self._tasks:
                task = self._loop.create_task(self._listen(endpoint, sub_msg, callback))
                self._tasks[endpoint] = task
                self._queues[endpoint] = asyncio.Queue()
                self._events[endpoint] = asyncio.Event(loop=self._loop)

        self._loop.call_soon_threadsafe(_subscribe)

    def unsubscribe(self, endpoint):
        def _unsubscribe():
            event = self._events.pop(endpoint, None)
            if event is not None:
                event.set()
            task = self._tasks.pop(endpoint, None)
            if task is not None:
                task.cancel()

        self._loop.call_soon_threadsafe(_unsubscribe)

    def queue(self, endpoint, message):
        def _queue():
            queue = self._queues.get(endpoint, None)
            if queue is not None:
                queue.put_nowait(message)

        self._loop.call_soon_threadsafe(_queue)

    async def _listen(self, endpoint, sub_msg, callback):
        url = f"{self._url}{endpoint}"
        try:
            ws = await websockets.connect(url, loop=self._loop)
            await self._welcome(ws)
            await self._confirm(ws, sub_msg)
            await self._handle(endpoint, ws, callback)
        except asyncio.CancelledError:
            logging.info(f"{endpoint} has been canceled")
        except CosmosAsyncStop:
            logging.error(f"stopping {endpoint}")
        except CosmosAsyncError as e:
            logging.error(f"failed connection {endpoint}, {e}")
        except Exception as e:
            logging.exception(e)
            await asyncio.sleep(2, loop=self._loop)
        finally:
            self._tasks.pop(endpoint, None)
            self._queues.pop(endpoint, None)
            self._events.pop(endpoint, None)

    @staticmethod
    async def _welcome(ws):
        data = await ws.recv()
        data = json.loads(data)
        if data["type"] != "welcome":
            raise CosmosAsyncError("failed to get welcome message")

    @staticmethod
    async def _confirm(ws, sub_msg):
        json_msg = json.dumps(sub_msg)
        logging.debug(f"sending: {json_msg}")
        await ws.send(json_msg)
        data = await ws.recv()
        data = json.loads(data)
        logging.debug(f"recv: {data}")

    async def _handle(self, endpoint, ws, callback):
        queue = self._queues[endpoint]
        event = self._events[endpoint]
        while event.is_set() is False or self._stop_event.is_set() is False:
            await self._send(queue, ws)
            data = await ws.recv()
            data = json.loads(data)
            callback(data)
    
    @staticmethod
    async def _send(queue, ws):
        try:
            message = queue.get_nowait()
            if message is not None:
                logging.debug(f"sending: {message}")
                await ws.send(json.dumps(message))
            else:
                raise CosmosAsyncStop()
        except asyncio.QueueEmpty:
            pass
        except Exception:
            pass
