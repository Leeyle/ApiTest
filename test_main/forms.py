# -*- coding:utf-8 -*-
# /user/bin/python
# @Time   : 2018/7/26 17:23
# @Author : liyongle
# @File   : forms.py

from django.forms import Form
from django.forms import fields
from django.forms import widgets
from api.models import *
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re


class LoginForm(Form):

    username = fields.CharField(
        required=True,
        error_messages={"required": "用户名不能为空！", "invalid":"输入不符合规则！"},
        widget=widgets.TextInput(attrs={"class": "form-control", "id": "exampleInputEmail1", "placeholder": "请输入用户名"})
    )
    password = fields.CharField(
        required=True,
        error_messages={"required": "密码不能为空！", "invalid":"输入不符合规则！"},
        widget=widgets.TextInput(attrs={"class":"form-control", "id":"exampleInputPassword1", "placeholder":"请输入登录密码"})
    )
