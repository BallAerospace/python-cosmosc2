import platform
import subprocess
from cosmosc2.json_drb_object import *
import cosmosc2.top_level
from cosmosc2.script.script import *

###########################
# Telemetry Screen methods
###########################

# Get the organized list of available telemetry screens
def get_screen_list(config_filename=None, force_refresh=False):
    return cosmosc2.script.script.cmd_tlm_server.write(
        "get_screen_list", config_filename, force_refresh
    )


# Get a specific screen definition
def get_screen_definition(screen_full_name, config_filename=None, force_refresh=False):
    return cosmosc2.script.script.cmd_tlm_server.write(
        "get_screen_definition", screen_full_name, config_filename, force_refresh
    )
