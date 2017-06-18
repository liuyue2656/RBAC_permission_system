#!/usr/bin/env python
# coding: utf-8
# author: Liu Yue
# e-mail: liuyue@qding.me
# Pw @ 2016-07-07 16:58


from . import dashboard
from flask import (
    render_template,
    redirect,
    url_for,
    request,
    session,
    flash
)
from flask_login import login_required, current_user
from ..utils import permit_required


@dashboard.route("/", methods=["GET", "POST"])
@login_required
def index():
    return render_template("dashboard/index.html")
