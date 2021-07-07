#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
limits.py
"""

# Copyright 2021 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt

from cosmosc2 import conneciton

def get_out_of_limits():
    return conneciton.write("get_out_of_limits")


def get_overall_limits_state(ignored_items=None):
    return conneciton.write(
        "get_overall_limits_state", ignored_items
    )


def limits_enabled(*args):
    return conneciton.write("limits_enabled?", *args)


def enable_limits(*args):
    return conneciton.write("enable_limits", *args)


def disable_limits(*args):
    return conneciton.write("disable_limits", *args)


def get_stale(with_limits_only=False, target_name=None):
    return conneciton.write(
        "get_stale", with_limits_only, target_name
    )


def get_limits(target_name, packet_name, item_name, limits_set=None):
    return conneciton.write(
        "get_limits", target_name, packet_name, item_name, limits_set
    )


def set_limits(
    target_name,
    packet_name,
    item_name,
    red_low,
    yellow_low,
    yellow_high,
    red_high,
    green_low=None,
    green_high=None,
    limits_set="CUSTOM",
    persistence=None,
    enabled=True,
):
    return conneciton.write(
        "set_limits",
        target_name,
        packet_name,
        item_name,
        red_low,
        yellow_low,
        yellow_high,
        red_high,
        green_low,
        green_high,
        limits_set,
        persistence,
        enabled,
    )


def get_limits_groups():
    return conneciton.write("get_limits_groups")


def enable_limits_group(group_name):
    return conneciton.write(
        "enable_limits_group", group_name
    )


def disable_limits_group(group_name):
    return conneciton.write(
        "disable_limits_group", group_name
    )


def get_limits_sets():
    return conneciton.write("get_limits_sets")


def set_limits_set(limits_set):
    return conneciton.write("set_limits_set", limits_set)


def get_limits_set():
    return conneciton.write("get_limits_set")


def subscribe_limits_events(queue_size=1000):
    return conneciton.write(
        "subscribe_limits_events", queue_size
    )


def unsubscribe_limits_events(id_):
    return conneciton.write("unsubscribe_limits_events", id_)


def get_limits_event(id_, non_block=False):
    return conneciton.write(
        "get_limits_event", id_, non_block
    )
