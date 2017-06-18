#!/usr/bin/env python
# coding: utf-8
# author: Liu Yue
# e-mail: liuyue@qding.me
# Pw @ 2016-07-07 16:58

# 仪表盘


from flask import Blueprint

dashboard = Blueprint("dashboard", __name__)

from . import views, events