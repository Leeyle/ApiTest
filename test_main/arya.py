# -*- coding:utf-8 -*-
# /user/bin/python
# @Time   : 2018/7/30 19:14
# @Author : liyongle
# @File   : arya.py

from arya.service import warrior
from django.utils.safestring import mark_safe
from . import models

class UserMainConfig(object):

    def get_show_add(self):
        code_list  = self.request.permission_code_list
        if 'add' in code_list:
            return True

    def git_list_display(self):
        code_list = self.request.permission_code_list
        result = []
        result.extend(self.list_display):
        

