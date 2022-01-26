#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
cosmos_v5_stream_example.py
"""
import argparse
from datetime import datetime
import os
import json
import logging
from threading import Event
import time

# See cosmosc2/docs/environment.md for environment documentation

os.environ["COSMOS_VERSION"] = "1.1.1"
os.environ["COSMOS_API_PASSWORD"] = "www"
os.environ["COSMOS_LOG_LEVEL"] = "INFO"
os.environ["COSMOS_WS_SCHEMA"] = "ws"
os.environ["COSMOS_API_HOSTNAME"] = "127.0.0.1"
os.environ["COSMOS_API_PORT"] = "2900"

from cosmosc2.stream import CosmosAsyncStream
from cosmosc2.stream_api import CosmosAsyncClient

EVENT = Event()
DATA = []


def datetime_value(dt: datetime = None):
    if dt is None:
        dt = datetime.now()
    return int(dt.timestamp() * 1000000000)


def output_data_to_file():
    if not DATA:
        return
    filename = f"{datetime_value()}.csv"
    with open(filename, "w") as f:
        f.write("ITEM,VALUE,TIME\n")
        for data in DATA:
            f.write(f"{data['item']},{data['value']},{data['time']}\n")
    print(filename)


def split_data(message):
    for data in json.loads(message):
        t = data.pop("time")
        for item, value in data.items():
            DATA.append({
                "item": item,
                "value": value,
                "time": t,
            })


def extract_data(message: dict):
    msg = message.get("message")
    typ = message.get("type")
    if msg == '[]':
        EVENT.set()
    elif typ is None and msg is not None:
        split_data(msg)


def validate_args(parser: argparse.ArgumentParser):
    args = parser.parse_args()
    mode = args.mode
    start_time = datetime.strptime(
        args.start, "%Y/%m/%d %H:%M:%S"
    )
    end_time = datetime.strptime(
        args.end, "%Y/%m/%d %H:%M:%S"
    )
    items = []
    
    for item in args.items:
        item_list = item.split("__")
        if len(item_list) != 3:
            raise ValueError(
                f"incorrect item format: {item}"
            )
        item_list.insert(0, "TLM")
        item_list.append(mode)
        items.append("__".join(item_list))

    return {
        "mode": mode,
        "start_time": datetime_value(start_time),
        "end_time": datetime_value(end_time),
        "items": items,
    }

# item example: INST__ADCS__POSX
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode",
        type=str,
        choices=["CONVERTED", "DECOM", "RAW"],
        help="item mode"
    )
    parser.add_argument(
        "start",
        type=str,
        help="start time in format: '2022/01/24 11:04:19'"
    )
    parser.add_argument(
        "end",
        type=str,
        help="end time in format: '2022/01/25 11:04:19'"
    )
    parser.add_argument(
        "items",
        type=str,
        nargs="+",
        help="item in format: TLM__INST__ADCS__POSX__CONVERTED"
    )

    try:
        kwargs = validate_args(parser)
    except ValueError as e:
        logging.error(e)
        return

    stream = CosmosAsyncStream()
    stream.start()

    client = CosmosAsyncClient(stream)
    client.streaming_channel_sub(extract_data)

    logging.debug(f"request being sent with: {kwargs}")
    client.streaming_channel_add(**kwargs)

    try:
        while not EVENT.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        EVENT.set()

    client.streaming_channel_unsub()
    stream.stop()

    output_data_to_file()   


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as err:
        logging.exception(err)
