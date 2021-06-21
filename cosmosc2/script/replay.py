from cosmosc2.script.script import *


def replay_select_file(filename, packet_log_reader="DEFAULT"):
    return cosmosc2.script.script.cmd_tlm_server.write(
        "replay_select_file", filename, packet_log_reader
    )


def replay_status():
    return cosmosc2.script.script.cmd_tlm_server.write("replay_status")


def replay_set_playback_delay(delay):
    return cosmosc2.script.script.cmd_tlm_server.write(
        "replay_set_playback_delay", delay
    )


def replay_play():
    return cosmosc2.script.script.cmd_tlm_server.write("replay_play")


def replay_reverse_play():
    return cosmosc2.script.script.cmd_tlm_server.write("replay_reverse_play")


def replay_stop():
    return cosmosc2.script.script.cmd_tlm_server.write("replay_stop")


def replay_step_forward():
    return cosmosc2.script.script.cmd_tlm_server.write("replay_step_forward")


def replay_step_back():
    return cosmosc2.script.script.cmd_tlm_server.write("replay_step_back")


def replay_move_start():
    return cosmosc2.script.script.cmd_tlm_server.write("replay_move_start")


def replay_move_end():
    return cosmosc2.script.script.cmd_tlm_server.write("replay_move_end")


def replay_move_index(index):
    return cosmosc2.script.script.cmd_tlm_server.write("replay_move_index", index)
