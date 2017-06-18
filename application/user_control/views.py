#!/usr/bin/env python
# coding: utf-8
# author: Liu Yue
# e-mail: liuyue@qding.me
# blog: http://liuyue.club
# Pw @ 2017-02-07 16:54:10

from datetime import datetime
from flask import render_template, redirect, url_for, request, session, flash, current_app
from flask_login import current_user, login_required, logout_user

from . import user_control
from forms import ChangePassword, OpsUser, OpsRole, OpsPermission, OpsMenu
from application import db
from application.models.user import User, Role, Permission, Menu
from application.utils import permit_required


@user_control.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePassword()
    if form.validate_on_submit():
        data_obj = User.query.filter_by(id=current_user.id).first()
        data_obj.password = form.password.data
        db.session.merge(data_obj)
        logout_user()
        return redirect(url_for("auth.login_page"))
    return render_template("user_control/change_password.html", form=form)


# NOTE 用户管理


@user_control.route("/user/", methods=["GET", "POST"])
@login_required
@permit_required("user_manager")
def user_index():
    users = User.query.all()
    current_app.logger.debug("test")
    current_app.logger.warning("test")
    current_app.logger.info("test")
    current_app.logger.error("test")
    return render_template("user_control/user.html", users=users)


@user_control.route("/user/create/", methods=["GET", "POST"])
@login_required
@permit_required("user_manager")
def user_create():
    form = OpsUser(is_update=False)
    if form.validate_on_submit():
        user = User()
        user.password = "password"
        for field in form:
            if field.name not in ("csrf_token", "submit"):
                user.__setattr__(field.name, field.data)
        return redirect(url_for(".user_index"))
    return render_template("user_control/user_create.html", form=form)


@user_control.route("/user/update/", methods=["GET", "POST"])
@login_required
# @permit_required("user_control")
def user_update():
    form = OpsUser()
    user = User.query.filter_by(id=request.args.get("id")).first()
    if form.validate_on_submit():
        for field in form:
            if field.name not in ("csrf_token", "submit"):
                user.__setattr__(field.name, field.data)
        return redirect(url_for(".user_index"))
    return render_template("user_control/user_update.html", form=form,
                           user=user, getattr=getattr)


@user_control.route("/user/delete/", methods=["POST"])
@login_required
# @permit_required("user_control")
def user_delete():
    list_id = request.get_data()
    user = User.query.filter_by(id=list_id).first()
    db.session.delete(user)
    return redirect(url_for(".user_index"))


# NOTE 角色管理


@user_control.route("/role/")
@login_required
def role_index():
    roles = Role.query.all()
    return render_template("user_control/role.html", roles=roles)


@user_control.route("/role/create/", methods=["GET", "POST"])
@login_required
@permit_required("user_manager")
def role_create():
    form = OpsRole()
    if form.validate_on_submit():
        role = Role()
        for field in form:
            if field.name not in ("csrf_token", "submit",):
                role.__setattr__(field.name, field.data)
        return redirect(url_for(".role_index"))
    return render_template("user_control/role_create.html", form=form)


@user_control.route("/role/update/", methods=["GET", "POST"])
@login_required
# @permit_required("user_control")
def role_update():
    form = OpsRole()
    role = Role.query.filter_by(id=request.args.get("id")).first()
    if form.validate_on_submit():
        for field in form:
            if field.name not in ("csrf_token", "submit",):
                role.__setattr__(field.name, field.data)
        return redirect(url_for(".role_index"))
    return render_template("user_control/role_update.html", form=form,
                           role=role, getattr=getattr)


@user_control.route("/role/delete/", methods=["POST"])
@login_required
# @permit_required("user_control")
def role_delete():
    list_id = request.get_data()
    role = Role.query.filter_by(id=list_id).first()
    db.session.delete(role)
    return redirect(url_for(".role_index"))


# NOTE 权限管理


@user_control.route("/permission/")
@login_required
def permission_index():
    permissions = Permission.query.all()
    return render_template("user_control/permission.html",
                           permissions=permissions)


@user_control.route("/permission/create/", methods=["GET", "POST"])
@login_required
@permit_required("user_manager")
def permission_create():
    form = OpsPermission()
    if form.validate_on_submit():
        permission = Permission()
        for field in form:
            if field.name not in ("csrf_token", "submit"):
                permission.__setattr__(field.name, field.data)
            permission.create = datetime.today()
        return redirect(url_for(".permission_index"))
    return render_template("user_control/permission_create.html", form=form)


@user_control.route("/permission/update/", methods=["GET", "POST"])
@login_required
# @permit_required("user_control")
def permission_update():
    form = OpsPermission()
    permission = Permission.query.filter_by(id=request.args.get("id")).first()
    if form.validate_on_submit():
        for field in form:
            if field.name not in ("csrf_token", "submit"):
                permission.__setattr__(field.name, field.data)
        return redirect(url_for(".permission_index"))
    return render_template("user_control/permission_update.html", form=form,
                           permission=permission, getattr=getattr)


@user_control.route("/permission/delete/", methods=["POST"])
@login_required
# @permit_required("user_control")
def permission_delete():
    list_id = request.get_data()
    permission = Permission.query.filter_by(id=list_id).first()
    db.session.delete(permission)
    return redirect(url_for(".permission_index"))


# NOTE 菜单管理


@user_control.route("/menu/", methods=["GET", "POST"])
@login_required
@permit_required("user_manager")
def menu_index():
    menus = Menu.query.order_by(Menu.pid, Menu.display_order).all()
    return render_template("user_control/menu.html", menus=menus, Menu=Menu)


@user_control.route("/menu/create/", methods=["GET", "POST"])
@login_required
@permit_required("user_manager")
def menu_create():
    form = OpsMenu()
    if form.validate_on_submit():
        menu = Menu()
        for field in form:
            if field.name not in ("csrf_token", "submit", "pid"):
                menu.__setattr__(field.name, field.data)
        menu.pid = form.pid.data.id
        db.session.add(menu)
        return redirect(url_for(".menu_index"))
    return render_template("user_control/menu_create.html", form=form)


@user_control.route("/menu/update/", methods=["GET", "POST"])
@login_required
# @permit_required("user_control")
def menu_update():
    form = OpsMenu()
    menu = Menu.query.filter_by(id=request.args.get("id")).first()
    if form.validate_on_submit():
        for field in form:
            if field.name not in ("csrf_token", "submit", "pid"):
                menu.__setattr__(field.name, field.data)
            menu.pid = form.pid.data.id
        return redirect(url_for(".menu_index"))
    return render_template("user_control/menu_update.html", form=form,
                           menu=menu, getattr=getattr)


@user_control.route("/menu/delete/", methods=["POST"])
@login_required
# @permit_required("user_control")
def menu_delete():
    list_id = request.get_data()
    menu = Menu.query.filter_by(id=list_id).first()
    db.session.delete(menu)
    return redirect(url_for(".menu_index"))
