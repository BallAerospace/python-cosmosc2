#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
cosmos_v5_stream_example.py
"""

import os
import time
import logging

# See cosmosc2/docs/environment.md for environment documentation

os.environ["COSMOS_VERSION"] = "1.1.1"
os.environ["COSMOS_API_PASSWORD"] = "www"
os.environ["COSMOS_LOG_LEVEL"] = "DEBUG"
os.environ["COSMOS_API_SCHEMA"] = "http"
os.environ["COSMOS_API_HOSTNAME"] = "127.0.0.1"
os.environ["COSMOS_API_PORT"] = "2900"

from cosmosc2.stream import CosmosAsyncStream
from cosmosc2.stream_api import CosmosAsyncClient


def log_func(message):
	logging.info(message)


stream = CosmosAsyncStream(schema="ws", hostname="localhost", port=2900)

logging.info('starting client')
stream.start()

client = CosmosAsyncClient(stream)

client.message_channel_sub(1, log_func)

try:
    time.sleep(5)
except KeyboardInterrupt:
    pass
except Exception:
    pass

client.message_channel_unsub()

stream.stop()
