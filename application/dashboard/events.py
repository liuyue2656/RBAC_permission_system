#!/usr/bin/env python
# coding: utf-8
# author: Liu Yue
# e-mail: liuyue@qding.me
# Pw @ 2016-09-19 12:06


from .. import socketio
import time


@socketio.on("connect", namespace="/print_log")
def print_log_connect():
    socketio.emit("print_log", {"data": "connect"}, namespace="/print_log")


@socketio.on("print_log", namespace="/print_log")
def print_log_event(message):
    test_list = [x for x in range(10)]
    print message["data"]
    while test_list:
        socketio.emit("test", {"data": "test%s" % test_list.pop(0)}, namespace="/print_log")
        time.sleep(0.1)
    time.sleep(1)
    socketio.emit("test", {"data": "down"}, namespace="/print_log")
