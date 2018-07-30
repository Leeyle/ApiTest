from django.db import models

# 菜单组
class Menu(models.Model):

    title = models.CharField(verbose_name='菜单组', max_length=32)

    class Meta:
        verbose_name_plural = '菜单表'

    def __str__(self):
        return self.title


# 权限组
class Group(models.Model):
    title = models.CharField(verbose_name='权限标题', max_length=32)
    menu = models.ForeignKey(verbose_name='所属菜单', to='Menu', default=1)

    class Meta:
        verbose_name_plural= '权限组表'

    def __str__(self):
        return self.title


# 权限表
class Permission(models.Model):

    title = models.CharField(verbose_name='标题', max_length=128)
    url = models.CharField(verbose_name='含正则表达式的URL', max_length=128)
    menu_gp = models.ForeignKey(verbose_name='组内权限', to='Permission', null=True, blank=True, related_name='x1')
    code = models.CharField(verbose_name='权限代号', max_length=32)
    group = models.ForeignKey(verbose_name='所属组', to='Group')

    class Meta:
        verbose_name_plural= '权限表'

    def __str__(self):
        return self.title

# 用户表
class UserInfo(models.Model):

    # username = models.CharField(verbose_name='用户名', max_length=32)
    # password = models.CharField(verbose_name='密码', max_length=64)
    # telephone = models.CharField(verbose_name='手机号', max_length=11)
    # email = models.EmailField(verbose_name='邮箱', max_length=32)
    name = models.CharField(verbose_name='真实姓名', max_length=32)
    user_role = models.ManyToManyField(verbose_name='用户角色', to='Role', blank=True)

    class Meta:
        verbose_name_plural= '用户表'

    def __str__(self):
        return self.name

# 角色表
class Role(models.Model):

    position = models.CharField(verbose_name='职位', max_length=32)
    permissions = models.ManyToManyField(verbose_name='角色权限', to='Permission', blank=True)

    class Meta:
        verbose_name_plural= '角色表'

    def __str__(self):
        return self.position
