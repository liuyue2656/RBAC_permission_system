#!/usr/bin/env python
# coding: utf-8
# author: Liu Yue
# e-mail: liuyue@qding.me
# blog: http://liuyue.club
# Pw @ 2017-02-07 16:54:32

from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, IntegerField,
                     SubmitField, SelectField)
from wtforms.validators import Required, Length, Email, EqualTo
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import (QuerySelectField,
                                           QuerySelectMultipleField)
from flask_login import current_user
from application.models.user import User, Role, Permission, Menu


class ChangePassword(FlaskForm):
    u"""
    更改密码
    """
    old_password = PasswordField(u"现在的密码", validators=[Required()])
    password = PasswordField(
        u"设置新密码",
        validators=[Required(),
                    EqualTo("password2", message="Password must match.")]
    )
    password2 = PasswordField(u"重复新密码", validators=[Required()])
    submit = SubmitField(u"确认")

    def validate_old_password(self, field):
        if not current_user.check_password(field.data):
            raise ValidationError(u"密码错误")


class OpsUser(FlaskForm):
    u"""
    用户信息
    """
    email = StringField(u"Email",
                        validators=[Required(), Length(10, 64), Email()])
    username = StringField(u"用户名", validators=[Required(), Length(1, 64)])
    tel_num = StringField(u"手机号码", validators=[Required(), Length(11, 11)])
    status = BooleanField(u"是否启用", default=True)
    roles = QuerySelectMultipleField(
        u"权限所属",
        query_factory=lambda: Role.query.all(),
        get_pk=lambda x: x.id,
        get_label=lambda x: x.display_name,
        validators=[Required()]
    )
    submit = SubmitField(u"确认")

    def __init__(self, is_update=True):
        super(OpsUser, self).__init__()
        # NOTE is_update为False时执行验证表单
        self.is_update = is_update

    def validate_email(self, field):
        if self.is_update:
            return True
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")

    def validate_username(self, field):
        if self.is_update:
            return True
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already in use.")

    def validate_tel_num(self, field):
        if self.is_update:
            return True
        if User.query.filter_by(tel_num=field.data).first():
            raise ValidationError("Username already in use.")


class OpsRole(FlaskForm):
    u"""
    角色操作
    """
    name = StringField(u"角色名称", validators=[Required()])
    display_name = StringField(u"显示名称", validators=[Required()])
    status = BooleanField(u"是否启用", validators=[Required()], default=True)
    permissions = QuerySelectMultipleField(
        u"权限列表",
        query_factory=lambda: Permission.query.all(),
        get_pk=lambda x: x.id,
        get_label=lambda x: x.name,
    )
    submit = SubmitField(u"确认")


class OpsPermission(FlaskForm):
    u"""
    权限操作
    """
    name = StringField(u"权限名称", validators=[Required()])
    operation_type = StringField(u"操作类型", validators=[Required()])
    menus = QuerySelectMultipleField(
        u"菜单列表",
        query_factory=lambda: Menu.query.all(),
        get_pk=lambda x: x.id,
        get_label=lambda x: x.title,
        validators=[Required()]
    )
    submit = SubmitField(u"确认")


class OpsMenu(FlaskForm):
    u"""
    菜单操作
    """
    name = StringField(u"菜单名称", validators=[Required()])
    title = StringField(u"菜单显示", validators=[Required()])
    pid = QuerySelectField(
        u"父菜单ID",
        query_factory=lambda: Menu.query.filter(Menu.pid == 0,
                                                Menu.url == None).all(),
        get_pk=lambda x: x.id,
        get_label=lambda x: x.title,
        allow_blank=True, blank_text=u'请选择'
    )
    url = StringField(u"菜单地址")
    display_order = IntegerField(u"显示顺序", validators=[Required()])
    submit = SubmitField(u"确认")
