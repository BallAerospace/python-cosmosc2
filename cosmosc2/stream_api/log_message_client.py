#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
data_extractor_client.py
"""

# Copyright 2022 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt

from datetime import datetime
import json

from cosmosc2.stream import CosmosAsyncStream
from cosmosc2.stream_api.base_client import BaseClient
from cosmosc2.stream_shared import CosmosAsyncClient


class LogMessageClient(BaseClient):

    def __init__(
        self,
        count: int,
        timeout: int = 30,
    ) -> None:
        super().__init__(timeout=timeout)
        self.count = count
        self._count = 0

    @staticmethod
    def _datetime_value(dt: datetime = None):
        if dt is None:
            dt = datetime.now()
        return int(dt.timestamp() * 1000000000)

    def _split_data(self, message):
        for data in json.loads(message):
            self._count += 1
            self._data.append(data)

    def _extract_data(self, message: dict):
        msg = message.get("message")
        typ = message.get("type")
        if self._count == self.count:
            self._event.set()
        elif typ is None and msg is not None:
            self._last_msg = datetime.now().timestamp()
            self._split_data(msg)

    def get(self):
        if self._data:
            return self._data

        stream = CosmosAsyncStream()
        stream.start()

        client = CosmosAsyncClient(stream)
        client.message_channel_sub(0, self._extract_data)

        self.wait()

        client.message_channel_unsub()
        stream.stop()

        return self._data
