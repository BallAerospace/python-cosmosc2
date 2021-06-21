import os

import cosmosc2.top_level
from cosmosc2.json_drb_object import *


class CheckError(RuntimeError):
    pass


class StopScript(RuntimeError):
    pass


class SkipTestCase(RuntimeError):
    pass


class HazardousError(RuntimeError):
    pass


cmd_tlm_server = None


def update_scope(scope: str):
    global cmd_tlm_server
    cmd_tlm_server.scope = str(scope)
    os.environ["COSMOS_SCOPE"] = str(scope)


def initialize_script_module(hostname=None, port=None):
    global cmd_tlm_server

    if cmd_tlm_server:
        cmd_tlm_server.disconnect()

    if hostname and port:
        cmd_tlm_server = JsonDRbObject(hostname, port)
    else:
        cmd_tlm_server = JsonDRbObject()


def shutdown_cmd_tlm():
    cmd_tlm_server.shutdown()


def script_disconnect():
    cmd_tlm_server.disconnect()


initialize_script_module()

from cosmosc2.script.extract import *
from cosmosc2.script.scripting import *
from cosmosc2.script.telemetry import *
from cosmosc2.script.commands import *
from cosmosc2.script.cmd_tlm_server import *
from cosmosc2.script.replay import *
from cosmosc2.script.limits import *
from cosmosc2.script.tools import *
from cosmosc2.script.api_shared import *
