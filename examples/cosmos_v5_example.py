from importlib.metadata import metadata
import os
import sys

# See cosmosc2/docs/environment.md for environment documentation

os.environ["COSMOS_VERSION"] = "1.1.1"
os.environ["COSMOS_API_PASSWORD"] = "password"
os.environ["COSMOS_LOG_LEVEL"] = "INFO"
os.environ["COSMOS_API_SCHEMA"] = "http"
os.environ["COSMOS_API_HOSTNAME"] = "127.0.0.1"
os.environ["COSMOS_API_PORT"] = "2900"

from cosmosc2 import *

status = cosmos_status()
print(status)
health = cosmos_health()

m = cosmos_metadata()
print(m)

d = cosmos_get_metadata("DEFAULT")
print(d)

c = cosmos_search_metadata("version", "0")
print(c)

c = cosmos_search_metadata("version", "1")
print(c)

v = cosmos_show_metadata('1234')
print(v)

n = cosmos_narrative()
print(n)

# ~ # telemetry.py
print(tlm("INST HEALTH_STATUS TEMP1"))
print(tlm_raw("INST HEALTH_STATUS TEMP1"))
print(tlm_formatted("INST HEALTH_STATUS TEMP1"))
print(tlm_with_units("INST HEALTH_STATUS TEMP1"))
print(tlm_variable("INST HEALTH_STATUS TEMP1", "RAW"))
print(set_tlm("INST HEALTH_STATUS TEMP1 = 5"))
print(get_tlm_packet("INST", "HEALTH_STATUS"))
print(
    get_tlm_values(
        [
            "INST__HEALTH_STATUS__TEMP1__CONVERTED",
            "INST__HEALTH_STATUS__TEMP2__CONVERTED",
        ]
    )
)
print(get_target_list())
print(get_target("INST"))
print(get_tlm_buffer("INST", "HEALTH_STATUS"))

id_ = subscribe_packets([["INST", "HEALTH_STATUS"]])
print(id_)

sys.exit(1)

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
# commands.py
cmd("INST ABORT")
cmd_no_range_check("INST COLLECT with TYPE NORMAL, TEMP 50.0")
cmd_no_hazardous_check("INST CLEAR")
cmd_no_checks("INST COLLECT with TYPE SPECIAL, TEMP 50.0")
cmd_raw("INST COLLECT with TYPE 0, TEMP 10.0")
cmd_raw_no_range_check("INST COLLECT with TYPE 0, TEMP 50.0")
cmd_raw_no_hazardous_check("INST CLEAR")
cmd_raw_no_checks("INST COLLECT with TYPE 1, TEMP 50.0")
send_raw("EXAMPLE_INT", "\x00\x00\x00\x00")
send_raw_file("EXAMPLE_INT", os.path.join(FILE_PATH, "test.txt"))
get_cmd_list("INST")
get_cmd_param_list("INST", "COLLECT")
get_cmd_hazardous("INST", "CLEAR")
get_cmd_value("INST", "COLLECT", "TEMP")
get_cmd_time()
get_cmd_buffer("INST", "COLLECT")
cmd_no_range_check("INST COLLECT with TYPE NORMAL, TEMP 50.0")


# timeline_api.py
print(cosmos_timelines())

update_scope("UPDATE")

shutdown()
