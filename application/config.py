#!/usr/bin/env python
# coding: utf-8
# author: Liu Yue
# e-mail: liuyue@qding.me
# Pw @ 2016-07-07 16:20


import os
import datetime
import logging

join = os.path.join
basedir = os.path.abspath(os.path.dirname(__file__))


class ProConfig():
    SECRET_KEY = ""
    SQLALCHEMY_DATABASE_URI = ""  # database like DevConfig
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY_EXPIRE_ON_COMMIT = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=60)
    LOG_LEVEL = logging.INFO
    LOG_FILE = join(basedir, "logs/access.log")


class DevConfig():
    DEBUG = True
    SECRET_KEY = ""
    SQLALCHEMY_DATABASE_URI = 'mysql://user:password@localhost:3306/db_name?charset=utf8'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=60)
    LOG_LEVEL = logging.DEBUG
    LOG_FILE = join(basedir, "logs/access.log")
