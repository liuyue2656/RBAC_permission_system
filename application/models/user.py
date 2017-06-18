#!/usr/bin/env python
# coding: utf-8
# author: Liu Yue
# e-mail: liuyue@qding.me
# blog: http://liuyue.club
# Pw @ 2016-07-07 16:19

# 用户权限数据库模型


from application import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# from . import relation_ship_select
import json
import collections
from base_model import MyModel


user_role = db.Table(
    "user_role",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"))
)

role_permission = db.Table(
    "role_permission",
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
    db.Column("permission_id", db.Integer, db.ForeignKey("permission.id"))
)

permission_menu = db.Table(
    "permission_menu",
    db.Column("permission_id", db.Integer, db.ForeignKey("permission.id")),
    db.Column("menu_id", db.Integer, db.ForeignKey("menu.id"))
)


class User(UserMixin, db.Model):
    u"""
    用户信息
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    username = db.Column(db.String(64), nullable=False)
    tel_num = db.Column(db.String(11), unique=True, nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=True)
    _password = db.Column(db.String(128), nullable=False)
    last = db.Column(db.DateTime)
    logs = db.relationship("Log", backref="user")
    roles = db.relationship("Role", secondary=user_role,
                            backref=db.backref("user", lazy="dynamic"))

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    def can(self, permission):
        # NOTE 验证权限
        if permission in [permission.name for role in self.roles
                                          for permission in role.permissions]:
            return True
        else:
            return False

    def generate_menu(self):
        # NOTE 生成用户个性化菜单
        menu_dict = collections.OrderedDict()
        child_menu = set()
        for role in self.roles:
            for permission in role.permissions:
                child_menu.update(permission.menus)
        parent_menu = child_menu & set(Menu.query.filter_by(pid=0).all())
        child_menu = child_menu - parent_menu
        parent_menu = sorted(parent_menu, key=lambda key: key.display_order)
        for menu in parent_menu:
            if menu.url:
                menu_dict[menu.title] = menu.url
            else:
                menu_dict[menu.title] = collections.OrderedDict()
                _menu = [m for m in child_menu if m.pid == menu.id]
                _menu = sorted(_menu, key=lambda key: key.display_order)
                for c_menu in _menu:
                    menu_dict[menu.title][c_menu.title] = c_menu.url
        return json.dumps(menu_dict)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model, MyModel):
    u"""
    角色表
    """
    __tablename__ = "role"
    name = db.Column(db.String(64), unique=True, nullable=False)
    display_name = db.Column(db.String(64), unique=True, nullable=False)
    permissions = db.relationship("Permission", secondary=role_permission,
                                  backref=db.backref("role", lazy="dynamic"))
    status = db.Column(db.Boolean, nullable=False, default=True)


class Permission(db.Model, MyModel):
    u"""
    权限表权
    """
    __tablename__ = "permission"
    name = db.Column(db.String(64), nullable=False)
    create = db.Column(db.DateTime, nullable=False)
    operation_type = db.Column(db.String(64), nullable=False)
    menus = db.relationship("Menu", secondary=permission_menu,
                            backref=db.backref("permission", lazy="dynamic"))


class Menu(db.Model, MyModel):
    u"""
    菜单表
    """
    __tablename__ = "menu"
    name = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(128), unique=True, nullable=False)
    # NOTE 父目录ID，0为顶级目录
    pid = db.Column(db.Integer, nullable=False, default=0)
    url = db.Column(db.String(256))
    display_order = db.Column(db.Integer, nullable=False)
    logs = db.relationship("Log", backref="menu")


class Log(db.Model, MyModel):
    u"""
    用户操作日志
    """
    __tablename__ = "log"
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    menu_id = db.Column(db.Integer, db.ForeignKey("menu.id"))
    operation_type = db.Column(db.String(64), nullable=False)
    operation_time = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.String(256), nullable=False)
    remarks = db.Column(db.String(256))
