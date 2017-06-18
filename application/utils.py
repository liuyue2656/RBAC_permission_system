#!/usr/bin/env python
# coding: utf-8
# author: Liu Yue
# e-mail: liuyue@qding.me
# blog: http://liuyue.club
# Pw @ 2016-08-12 15:50

from flask import abort, redirect, url_for, flash, g
from functools import wraps
from flask_login import current_user
from models.user import Permission
from flask import current_app
import subprocess
import xml.etree.ElementTree as xml_tree
import collections
import json


def permit_required(user_permission):
    def _deco(func):
        @wraps(func)
        def __deco(*args, **kwargs):
            if current_user.check_password("password"):
                flash(u"请修改初始密码")
                return redirect(url_for("user_control.change_password"))
            if not Permission.query.filter_by(name=user_permission).first():
                abort(401)
            if not current_user.can(user_permission):
                abort(403)
            return func(*args, **kwargs)
        return __deco
    return _deco


def init_root():
    from models.uesr import User, Role, Permission, Menu
    if not Role.query.filter_by(name="root").first():
        # NOTE 添加管理员角色
        if Role.query.filter_by(name="root").first():
            return
        root_role = Role(name="root", display_name="管理员")
    admin = User(
        email="liuyue@qding.me",
        username="刘越",
        tel_num="15010180356",
        password="password"
    )
    admin.roles.append(root_role)
    db.session.add(admin)
    db.session.commit()
