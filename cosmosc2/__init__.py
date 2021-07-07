#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
__init__.py
"""

# Copyright 2021 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt

import os
from cosmosc2.connection import Connection


conneciton = None


def update_scope(scope: str):
    global conneciton 
    conneciton.scope = str(scope)
    os.environ["COSMOS_SCOPE"] = str(scope)


def initialize_script_module(hostname=None, port=None):
    global conneciton 

    if conneciton:
        conneciton.disconnect()

    if hostname and port:
        conneciton = Connection(hostname, port)
    else:
        conneciton = Connection()


def shutdown_cmd_tlm():
    conneciton.shutdown()


def script_disconnect():
    conneciton.disconnect()


initialize_script_module()


from cosmosc2.api_shared import *
from cosmosc2.cmd_tlm_server import *
from cosmosc2.commands import *
from cosmosc2.extract import *
from cosmosc2.limits import *
from cosmosc2.telemetry import *
from cosmosc2.tools import *