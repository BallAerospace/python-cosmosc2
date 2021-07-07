import os
import sys

# See cosmosc2/docs/environment.md for environment documentation

os.environ["COSMOSC2_VERSION"] = "1.1.1"
os.environ["COSMOS_DEBUG"] = "DEBUG"
os.environ["COSMOS_SCHEMA"] = "http"
os.environ["COSMOS_HOSTNAME"] = "127.0.0.1"
os.environ["COSMOS_PORT"] = "2900"

from cosmosc2 import *

# ~ # telemetry.py
telemetry = [
    tlm("INST HEALTH_STATUS TEMP1"),
    tlm_raw("INST HEALTH_STATUS TEMP1"),
    tlm_formatted("INST HEALTH_STATUS TEMP1"),
    tlm_with_units("INST HEALTH_STATUS TEMP1"),
    tlm_variable("INST HEALTH_STATUS TEMP1", "RAW"),
    set_tlm("INST HEALTH_STATUS TEMP1 = 5"),
    set_tlm_raw("INST HEALTH_STATUS TEMP1 = 5"),
    get_tlm_packet("INST", "HEALTH_STATUS"),
    get_tlm_values(
        [["INST", "HEALTH_STATUS", "TEMP1"], ["INST", "HEALTH_STATUS", "TEMP2"]]
    ),
    get_tlm_list("INST"),
    get_tlm_item_list("INST", "HEALTH_STATUS"),
    get_target_list(),
    get_tlm_details(
        [["INST", "HEALTH_STATUS", "TEMP1"], ["INST", "HEALTH_STATUS", "TEMP2"]]
    ),
    get_tlm_buffer("INST", "HEALTH_STATUS"),
]
for i in telemetry:
    try:
        i.result
    except AttributeError:
        print(i)

id_ = subscribe_packet_data([["INST", "HEALTH_STATUS"]])
get_packet_data(id_)
unsubscribe_packet_data(id_)

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
# commands.py
commands = [
    cmd("INST ABORT"),
    cmd_no_range_check("INST COLLECT with TYPE NORMAL, TEMP 50.0"),
    cmd_no_hazardous_check("INST CLEAR"),
    cmd_no_checks("INST COLLECT with TYPE SPECIAL, TEMP 50.0"),
    cmd_raw("INST COLLECT with TYPE 0, TEMP 10.0"),
    cmd_raw_no_range_check("INST COLLECT with TYPE 0, TEMP 50.0"),
    cmd_raw_no_hazardous_check("INST CLEAR"),
    cmd_raw_no_checks("INST COLLECT with TYPE 1, TEMP 50.0"),
    send_raw("EXAMPLE_INT", "\x00\x00\x00\x00"),
    send_raw_file("EXAMPLE_INT", os.path.join(FILE_PATH, "test.txt")),
    get_cmd_list("INST"),
    get_cmd_param_list("INST", "COLLECT"),
    get_cmd_hazardous("INST", "CLEAR"),
    get_cmd_value("INST", "COLLECT", "TEMP"),
    get_cmd_time(),
    get_cmd_buffer("INST", "COLLECT"),
    cmd_no_range_check("INST COLLECT with TYPE NORMAL, TEMP 50.0"),
]
for i in commands:
    try:
        i.result
    except AttributeError:
        print(i)
        sys.exit(1)

update_scope("UPDATE")

script_disconnect()
shutdown_cmd_tlm()
