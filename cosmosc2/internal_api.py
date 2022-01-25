#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
internal_api.py
"""

# Copyright 2022 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt

import cosmosc2


def cosmos_status():
    """Get the cosmos status api.
    Syntax / Example:
        status = cosmos_status()
    """
    resp = cosmosc2.COSMOS.get(
        "/cosmos-api/internal/status", headers={"Accept": "application/json"}
    )
    return resp.json()


def cosmos_health():
    """Get the cosmos health api.
    Syntax / Example:
        health = cosmos_health()
    """
    resp = cosmosc2.COSMOS.get(
        "/cosmos-api/internal/health", headers={"Accept": "application/json"}
    )
    return resp.json()


def cosmos_metrics():
    """Get the cosmos metrics api.
    Syntax / Example:
        metrics = cosmos_metrics()
    """
    resp = cosmosc2.COSMOS.get(
        "/cosmos-api/internal/metrics", headers={"Accept": "plain/txt"}
    )
    return resp.text
