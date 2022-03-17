#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
calendar_api.py
"""

# Copyright 2022 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt

import cosmosc2


def cosmos_timelines():
    """Get the cosmos timeline api.
    Syntax / Example:
        timelines = cosmos_timelines()
    """
    resp = cosmosc2.COSMOS.get(
        "/cosmos-api/timeline",
        headers={"Accept": "application/json"}
    )
    return resp.json()


def cosmos_timeline_activities(timeline: str):
    """Get the cosmos health api.
    Syntax / Example:
        activities = cosmos_timeline_activities("alpha")
    """
    resp = cosmosc2.COSMOS.get(
        f"/cosmos-api/timeline/{timeline}/activities",
        headers={"Accept": "application/json"},
    )
    return resp.json()


def cosmos_timeline_activity_count(timeline: str):
    """Get the cosmos timeline activity count.
    Syntax / Example:
        count = cosmos_timeline_activity_count("alpha")
    """
    resp = cosmosc2.COSMOS.get(
        f"/cosmos-api/timeline/{timeline}/count",
        headers={"Accept": "plain/txt"}
    )
    return resp.text

def cosmos_metadata():
    resp = cosmosc2.COSMOS.get(
        "/cosmos-api/metadata",
        headers={"Accept": "application/json"},
    )
    return resp.json()

def cosmos_show_metadata(metadata_id):
    resp = cosmosc2.COSMOS.get(
        "".join(["/cosmos-api/metadata/",metadata_id]),
        headers={"Accept": "application/json"},
    )
    return resp.json()

def cosmos_search_metadata(key, value):
    resp = cosmosc2.COSMOS.get(
        "/cosmos-api/metadata/_search",
        headers={"Accept": "application/json"},
        params={"key": key, "value": value},
    )
    return resp.json()

def cosmos_get_metadata(name):
    resp = cosmosc2.COSMOS.get(
        "".join(["/cosmos-api/metadata/_get/", name]),
        headers={"Accept": "application/json"},
    )
    return resp.json()

def cosmos_narrative():
    resp = cosmosc2.COSMOS.get(
        "/cosmos-api/narrative",
        headers={"Accept": "application/json"},
    )
    return resp.json()

def cosmos_show_narrative(narrative_id):
    resp = cosmosc2.COSMOS.get(
        "".join(["/cosmos-api/narrative/", narrative_id]),
        headers={"Accept": "application/json"},
    )
    return resp.json()

def cosmos_search_narrative(q):
    resp = cosmosc2.COSMOS.get(
        "/cosmos-api/narrative/_search",
        headers={"Accept": "application/json"},
        params={"q": q},
    )
    return resp.json()
