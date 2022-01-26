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
import logging
from threading import Event
import time


class BaseClient:

    def __init__(self, timeout: int = 30) -> None:
        self._event = Event()
        self._data = []
        self._last_msg = datetime.now().timestamp()
        self._timeout = timeout

    def wait(self):
        try:
            while not self._event.is_set():
                time.sleep(1)
                current_time = datetime.now().timestamp()
                if (current_time - self._last_msg) > self._timeout:
                    self._event.set()
        except TimeoutError:
            logging.error(
                f"No messages have been sent for {self._timeout} seconds"
            )
        except KeyboardInterrupt:
            pass
