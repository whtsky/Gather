# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from flask import current_app, g, render_template, url_for
from flask.ext.mail import Message
from gather.form import Form
from wtforms import TextField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import Length, Email, DataRequired, Optional, URL, Regexp
from gather.utils import send_mail
from gather.account.models import Account
from gather.account.utils import login_user, create_reset_token


class LoginForm(Form):
    username = TextField("用户名", validators=[
        Length(max=15, message="用户名最多15个字符哟~"),
        DataRequired(),
        Regexp("^[a-zA-Z0-9]+$", message="用户名只能由英文字母和数字构成")
    ])
    password = PasswordField("密码", validators=[
        DataRequired()
    ])

    def validate_password(self, field):
        account = self.username.data
        user = Account.query.filter_by(username=account).first()

        if user and user.check_password(field.data):
            self.user = user
            return user
        raise ValueError("用户名或密码错误")

    def login(self):
        login_user(self.user)


class RegisterForm(LoginForm):
    email = TextField("电子邮件地址", validators=[
        Email(),
        DataRequired()
    ])

    def validate_password(self, field):
        return True

    def validate_username(self, field):
        if Account.query.filter_by(username=field.data.lower()).count():
            raise ValueError("这个用户名被注册了")

    def validate_email(self, field):
        if Account.query.filter_by(email=field.data.lower()).count():
            raise ValueError("这个电子邮件地址被注册了")

    def save(self):
        user = Account(**self.data)
        return user.save()


class FindForm(Form):
    email = TextField("电子邮件地址", validators=[
        Email(),
        DataRequired()
    ])

    def validate_email(self, field):
        if not Account.query.filter_by(email=field.data.lower()).count():
            raise ValueError("这个电子邮件地址尚未注册")

    def send(self):
        config = current_app.config
        email = self.email.data
        user = Account.query.filter_by(email=email.lower()).first_or_404()
        msg = Message(
            "找回 {username} 在 {site_name} 的密码".format(
                username=user.username,
                site_name=config["FORUM_TITLE"]
            ),
            recipients=[email],
        )
        reset_url = "".join([
            config["FORUM_URL"].rstrip("/"),
            url_for("account.reset"),
            "?token=",
            create_reset_token(user)
        ])
        msg.html = render_template('email/reset.html', user=user, url=reset_url)
        send_mail(msg)


class ResetForm(Form):
    password = PasswordField("密码", validators=[
        DataRequired()
    ])

    def reset(self, user):
        user.change_password(self.password.data)
        return user.save()


class SettingsForm(Form):
    username = TextField("用户名", validators=[
        Length(max=15, message="用户名最多15个字符哟~"),
        DataRequired(),
        Regexp("^[a-zA-Z0-9]+$", message="用户名只能由英文字母和数字构成")
    ])
    website = TextField("网站", validators=[
        URL(), Optional(), Length(max=100)
    ])
    email = TextField("电子邮件地址", validators=[
        Email(),
        DataRequired()
    ])
    feeling_lucky = BooleanField("手气不错")
    description = TextAreaField("简介", validators=[
        Optional(), Length(max=500)
    ], description="我叫王大锤，万万没想到..")
    css = TextAreaField("自定义 CSS", validators=[
        Optional()
    ], description="body{display: none}")

    def validate_username(self, field):
        user = Account.query.filter_by(username=field.data.lower()).first()
        if user and user.id != g.user.id:
            raise ValueError("这个用户名被注册了")

    def validate_email(self, field):
        user = Account.query.filter_by(email=field.data.lower()).first()
        if user and user.id != g.user.id:
            raise ValueError("这个电子邮件地址被注册了")

    def save(self):
        user = Account.query.get(g.user.id)
        self.populate_obj(user)
        user.save()
