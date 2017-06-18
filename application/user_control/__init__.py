#!/usr/bin/env python
# coding: utf-8
# author: Liu Yue
# e-mail: liuyue@qding.me
# blog: http://liuyue.club
# Pw @ 2017-02-07 16:53:36

# NOTE 权限管理


from flask import Blueprint

user_control = Blueprint("user_control", __name__)

from . import views
