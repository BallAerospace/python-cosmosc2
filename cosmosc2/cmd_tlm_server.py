#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: latin-1 -*-
"""
cmd_tlm_server.py
"""

# Copyright 2021 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt

from cosmosc2 import link

DEFAULT_SERVER_MESSAGES_QUEUE_SIZE = 1000


def get_interface_targets(interface_name):
    return link.json_rpc_request("get_interface_targets", interface_name)


def get_interface_names():
    return link.json_rpc_request("get_interface_names")


def connect_interface(interface_name, *params):
    return link.json_rpc_request("connect_interface", interface_name, *params)


def disconnect_interface(interface_name):
    return link.json_rpc_request("disconnect_interface", interface_name)


def interface_state(interface_name):
    return link.json_rpc_request("interface_state", interface_name)


def map_target_to_interface(target_name, interface_name):
    return link.json_rpc_request("map_target_to_interface", target_name, interface_name)


def get_router_names():
    return link.json_rpc_request("get_router_names")


def connect_router(router_name, *params):
    return link.json_rpc_request("connect_router", router_name, *params)


def disconnect_router(router_name):
    return link.json_rpc_request("disconnect_router", router_name)


def router_state(router_name):
    return link.json_rpc_request("router_state", router_name)


def get_target_info(target_name):
    return link.json_rpc_request("get_target_info", target_name)


def get_all_target_info():
    return link.json_rpc_request("get_all_target_info")


def get_target_ignored_parameters(target_name):
    return link.json_rpc_request("get_target_ignored_parameters", target_name)


def get_target_ignored_items(target_name):
    return link.json_rpc_request("get_target_ignored_items", target_name)


def get_interface_info(interface_name):
    return link.json_rpc_request("get_interface_info", interface_name)


def get_all_router_info():
    return link.json_rpc_request("get_all_router_info")


def get_all_interface_info():
    return link.json_rpc_request("get_all_interface_info")


def get_router_info(router_name):
    return link.json_rpc_request("get_router_info", router_name)


def get_all_cmd_info():
    return link.json_rpc_request("get_all_cmd_info")


def get_all_tlm_info():
    return link.json_rpc_request("get_all_tlm_info")


def get_cmd_cnt(target_name, command_name):
    return link.json_rpc_request("get_cmd_cnt", target_name, command_name)


def get_tlm_cnt(target_name, packet_name):
    return link.json_rpc_request("get_tlm_cnt", target_name, packet_name)


def get_packet_loggers():
    return link.json_rpc_request("get_packet_loggers")


def get_packet_logger_info(packet_logger_name):
    return link.json_rpc_request("get_packet_logger_info", packet_logger_name)


def get_all_packet_logger_info():
    return link.json_rpc_request("get_all_packet_logger_info")


def get_background_tasks():
    return link.json_rpc_request("get_background_tasks")


def start_background_task(task_name):
    return link.json_rpc_request("start_background_task", task_name)


def stop_background_task(task_name):
    return link.json_rpc_request("stop_background_task", task_name)


def get_server_status():
    return link.json_rpc_request("get_server_status")


def get_cmd_log_filename(packet_log_writer_name="DEFAULT"):
    return link.json_rpc_request("get_cmd_log_filename", packet_log_writer_name)


def get_tlm_log_filename(packet_log_writer_name="DEFAULT"):
    return link.json_rpc_request("get_tlm_log_filename", packet_log_writer_name)


def start_logging(packet_log_writer_name="ALL", label=None):
    return link.json_rpc_request("start_logging", packet_log_writer_name, label)


def stop_logging(packet_log_writer_name="ALL"):
    return link.json_rpc_request("stop_logging", packet_log_writer_name)


def start_cmd_log(packet_log_writer_name="ALL", label=None):
    return link.json_rpc_request("start_cmd_log", packet_log_writer_name, label)


def start_tlm_log(packet_log_writer_name="ALL", label=None):
    return link.json_rpc_request("start_tlm_log", packet_log_writer_name, label)


def stop_cmd_log(packet_log_writer_name="ALL"):
    return link.json_rpc_request("stop_cmd_log", packet_log_writer_name)


def stop_tlm_log(packet_log_writer_name="ALL"):
    return link.json_rpc_request("stop_tlm_log", packet_log_writer_name)


def start_raw_logging_interface(interface_name="ALL"):
    return link.json_rpc_request("start_raw_logging_interface", interface_name)


def stop_raw_logging_interface(interface_name="ALL"):
    return link.json_rpc_request("stop_raw_logging_interface", interface_name)


def start_raw_logging_router(router_name="ALL"):
    return link.json_rpc_request("start_raw_logging_router", router_name)


def stop_raw_logging_router(router_name="ALL"):
    return link.json_rpc_request("stop_raw_logging_router", router_name)


def get_server_message_log_filename():
    return link.json_rpc_request("get_server_message_log_filename")


def start_new_server_message_log():
    return link.json_rpc_request("start_new_server_message_log")


def subscribe_server_messages(queue_size=DEFAULT_SERVER_MESSAGES_QUEUE_SIZE):
    return link.json_rpc_request("subscribe_server_messages", queue_size)


def unsubscribe_server_messages(id_):
    return link.json_rpc_request("unsubscribe_server_messages", id_)


def get_server_message(id_, non_block=False):
    return link.json_rpc_request("get_server_message", id_, non_block)


def cmd_tlm_reload():
    return link.json_rpc_request("cmd_tlm_reload")


def cmd_tlm_clear_counters():
    return link.json_rpc_request("cmd_tlm_clear_counters")


def get_output_logs_filenames(filter_="*tlm.bin"):
    return link.json_rpc_request("get_output_logs_filenames", filter_)
