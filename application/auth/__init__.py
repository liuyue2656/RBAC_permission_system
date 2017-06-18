#!/usr/bin/env python
# coding: utf-8
# author: Liu Yue
# e-mail: liuyue@qding.me
# Pw @ 2016-07-07 16:08

# 用户认证


from flask import Blueprint

auth = Blueprint("auth", __name__)

from . import views
