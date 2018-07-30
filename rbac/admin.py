from django.contrib import admin
from . import models


#权限控制
admin.site.register(models.Menu)
admin.site.register(models.Group)
admin.site.register(models.Permission)
admin.site.register(models.UserInfo)
admin.site.register(models.Role)



