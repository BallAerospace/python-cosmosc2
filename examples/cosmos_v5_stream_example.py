#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
cosmos_v5_stream_example.py
"""
import argparse
from datetime import datetime
import os
import logging

# See cosmosc2/docs/environment.md for environment documentation

os.environ["COSMOS_VERSION"] = "1.1.1"
os.environ["COSMOS_API_PASSWORD"] = "password"
os.environ["COSMOS_LOG_LEVEL"] = "INFO"
os.environ["COSMOS_WS_SCHEMA"] = "ws"
os.environ["COSMOS_API_HOSTNAME"] = "127.0.0.1"
os.environ["COSMOS_API_PORT"] = "2900"

from cosmosc2.stream_api.data_extractor_client import DataExtractorClient

def output_data_to_file(data):
    if not data:
        return
    date_value = int(datetime.now().timestamp() * 1000000000)
    filename = f"{date_value}.csv"
    with open(filename, "w") as f:
        f.write("ITEM,VALUE,TIME\n")
        for d in data:
            f.write(f"{d['item']},{d['value']},{d['time']}\n")
    print(filename)


# item example: INST.ADCS.POSX
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
        help="item in format: INST.ADCS.POSX"
    )
    args = parser.parse_args()

    try:
        api = DataExtractorClient(
            items=args.items,
            start_time=args.start,
            end_time=args.end,
            mode=args.mode,
        )
        data = api.get()
        output_data_to_file(data)
    except ValueError as e:
        logging.error(e)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as err:
        logging.exception(err)
