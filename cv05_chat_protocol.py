#!/usr/bin/env python3
from enum import Enum

class Ctrl_value(Enum):
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    USERS = "USERS"
    MSG = "MSG"

class Chat_proto():
    def __init__(self, nick):
        self._nick = nick
        self._proto_template = "~{}~{}~{}~"
        self._users = list()
    def login(self):
        return self._proto_template.format(Ctrl_value.LOGIN.value, self._nick, "")
    def logout(self):
        return self._proto_template.format(Ctrl_value.LOGOUT.value, self._nick, "")
    def msg(self, text_msg):
        text_msg_sanitized = text_msg.replace("~", "")
        return self._proto_template.format(Ctrl_value.MSG.value, self._nick, text_msg_sanitized)
    def users(self):
        return self._proto_template.format(Ctrl_value.USERS.value, self._nick, "")
    def parse_proto_msg(self, proto_msg_text):
        proto_msg_list = proto_msg_text.split("~")
        if len(proto_msg_list) < 5:
            return False
        if proto_msg_list[1] == Ctrl_value.LOGIN.value:
            self._users.append(proto_msg_list[2])
            print("LOGIN user:" + proto_msg_list[2])
            return True
        elif proto_msg_list[1] == Ctrl_value.LOGOUT.value:
            self._users.remove(proto_msg_list[2])
            print("LOGOUT user:" + proto_msg_list[2])
            return True
        elif proto_msg_list[1] == Ctrl_value.MSG.value:
            print("MSG from {}: {}".format(proto_msg_list[2], proto_msg_list[3]))
            return True
        elif proto_msg_list[1] == Ctrl_value.USERS.value:
            print("USERS users:" + proto_msg_list[2])
            return self._users
        else:
            print("Unrecognized msg: " + proto_msg_list[1])
            return False
