#!/usr/bin/env python
# coding: utf-8
# author: Liu Yue
# e-mail: liuyue@qding.me
# blog: http://liuyue.club
# Pw @ 2016-07-07 16:12


from datetime import datetime
from flask import render_template, redirect, url_for, request, session, flash
from flask_login import current_user, login_required, login_user, logout_user

from . import auth
from forms import LoginForm, OpsUser, ChangePassword
from application import db
from application.models.user import User
from application.utils import permit_required


@auth.route("/")
def rewrite_root():
    return redirect(url_for(".login_page"))


@auth.route("/login", methods=["GET", "POST"])
def login_page():
    # NOTE 登录视图函数
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user.check_password(form.password.data):
            flash(u"密码错误")
            return redirect(url_for(".login_page"))
        else:
            login_user(user, form.remember_me.data)
            user.last = datetime.today()
            session.permanent = True
            return redirect(
                request.args.get("next") or url_for("dashboard.index")
            )
            current_user.menu = current_user.generate_menu()
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for(".login_page"))
