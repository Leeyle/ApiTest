from django.contrib import admin
from . import models

admin.site.register(models.UserMain)
admin.site.register(models.ObjManage)
admin.site.register(models.Square)
admin.site.register(models.ReqMethod)
admin.site.register(models.ApiRequest)
admin.site.register(models.TestCase)