#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
cosmos_v5_stream_example.py
"""
import argparse
import asyncio
from datetime import datetime
import os
import logging

# See cosmosc2/docs/environment.md for environment documentation

os.environ["COSMOS_VERSION"] = "1.1.1"
os.environ["COSMOS_API_PASSWORD"] = "www"
os.environ["COSMOS_LOG_LEVEL"] = "INFO"
os.environ["COSMOS_WS_SCHEMA"] = "ws"
os.environ["COSMOS_API_HOSTNAME"] = "127.0.0.1"
os.environ["COSMOS_API_PORT"] = "2900"

from cosmosc2.stream import CosmosAsyncStream
from cosmosc2.stream_api import CosmosAsyncClient

EVENT = asyncio.Event()


def extract_data(message: dict):
    msg = message.get("message")
    if msg is not None:
        logging.info(message)


def validate_args(parser: argparse.ArgumentParser):
    args = parser.parse_args()
    mode = args.mode
    items = []
    try:
        start = datetime.strptime(args.start, "%Y/%m/%d %H:%M:%S")
        end= datetime.strptime(args.start, "%Y/%m/%d %H:%M:%S")
    except ValueError as e:
        raise Exception(f"incorrect time input. {e}")
    
    for item in args.items:
        item_list = item.split("__")
        if len(item_list) != 3:
            raise Exception(f"incorrect item format: {item}")
        item_list.append(mode)
        items.append("__".join(item_list))

    return {
        "mode": mode,
        "start": start,
        "end": end,
        "items": items,
    }

# item example: INST__ADCS__POSX
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=str, choices=["CONVERTED", "DECOM", "RAW"], help="")
    parser.add_argument("start", type=str, help="start time in format: '2022/01/24 11:04:19'")
    parser.add_argument("end", type=str, help="end time in format: '2022/01/25 11:04:19'")
    parser.add_argument("items", type=str, nargs="+", help="item in format: TLM__INST__ADCS__POSX__CONVERTED")
    kwargs = validate_args(parser)

    stream = CosmosAsyncStream()
    stream.start()

    loop = asyncio.get_event_loop()

    client = CosmosAsyncClient(stream)
    client.streaming_channel_sub(extract_data)

    logging.info(f"request being sent with: {kwargs}")
    client.streaming_channel_add(**kwargs)

    try:
        loop.run_until_complete(EVENT.wait())
    except KeyboardInterrupt:
        EVENT.set()

    client.streaming_channel_unsub()
    stream.stop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as err:
        logging.exception(err)
