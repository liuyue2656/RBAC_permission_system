#!/usr/bin/env python
# coding: utf-8
# author: Liu Yue
# e-mail: liuyue@qding.me
# Pw @ 2016-07-07 16:36


from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, IntegerField,
                     SubmitField, SelectField)
from wtforms.validators import Required, Length, Email, EqualTo
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import (QuerySelectField,
                                           QuerySelectMultipleField)
from flask_login import current_user
from application.models.user import User, Role, Permission, Menu


class LoginForm(FlaskForm):
    u"""
    登陆表单
    """
    email = StringField(u"Email", validators=[Required(), Length(10, 64)])
    password = PasswordField(u"密码", validators=[Required()])
    remember_me = BooleanField(u"记住我")
    submit = SubmitField(u"确认登录")

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError(u"用户不存在")


class OpsUser(FlaskForm):
    u"""
    用户信息
    """
    email = StringField(u"Email",
                        validators=[Required(), Length(10, 64), Email()])
    username = StringField(u"用户名", validators=[Required(), Length(1, 64)])
    tel_num = StringField(u"手机号码", validators=[Required()])
    status = BooleanField(u"是否启用", default=True)
    roles_id = QuerySelectMultipleField(
        u"权限所属",
        query_factory=lambda: Role.query.all(),
        get_pk=lambda x: x.id,
        get_label=lambda x: x.name,
        allow_blank=True, blank_text=u'-- please choose --'
    )
    submit = SubmitField(u"确认")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already in use.")


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


class OpsPromission(FlaskForm):
    u"""
    权限操作
    """
    name = StringField(u"权限名称", validators=[Required()])
    operation_type = SelectField(u"操作类型", validators=[Required()])
    menus = QuerySelectMultipleField(
        u"菜单列表",
        query_factory=lambda: Menu.query.all(),
        get_pk=lambda x: x.id,
        get_label=lambda x: x.name,
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
        query_factory=lambda: Menu.query.filter_by(pid=0).all(),
        get_pk=lambda x: x.id,
        get_label=lambda x: x.name,
        allow_blank=True, blank_text=u'-- please choose --'
    )
    url = StringField(u"菜单地址", validators=[Required()])
    submit = SubmitField(u"确认")
