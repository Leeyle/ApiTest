from django.db import models
from rbac import models as rbac_model

# 用户表
class UserMain(models.Model):

    auth = models.OneToOneField(verbose_name='用户权限', to=rbac_model.UserInfo, null=True, blank=True)
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=128)
    telephone = models.CharField(verbose_name='手机号', max_length=11)
    email = models.EmailField(verbose_name='邮箱', max_length=32)

    class Meta:
        verbose_name_plural = '用户表'

    def __str__(self):
        return self.username

# 项目表
class ObjManage(models.Model):

    title = models.CharField(verbose_name='项目表', max_length=32)

    class Meta:
        verbose_name_plural = '项目表'

    def __str__(self):
        return self.title

# 模块表
class Square(models.Model):

    module_name = models.CharField(verbose_name='模块名称', max_length=32)
    menu = models.ForeignKey(verbose_name='所属项目', to='ObjManage', default=1)

    class Meta:
        verbose_name_plural = '模块表'

    def __str__(self):
        return self.Square

# 请求方式表
class ReqMethod(models.Model):

    method = models.CharField(verbose_name='请求方式', max_length=32)

    class Meta:
        verbose_name_plural = '请求方式表'

    def __str__(self):
        return self.method

# 接口表
class ApiRequest(models.Model):
    api_name = models.CharField(verbose_name='接口名称', max_length=32)
    api_url = models.CharField(verbose_name='ApiUrl', max_length=128)
    api_module = models.ForeignKey(verbose_name='接口所属模块', to='Square', default=1)
    api_agreement = models.CharField(verbose_name='接口协议', max_length=32)
    api_headers = models.CharField(verbose_name='请求头', max_length=128)

    class Meta:
        verbose_name_plural = '接口表'

    def __str__(self):
        return self.api_name

# 测试案例表
class TestCase(models.Model):
    case_module_id = models.ForeignKey(verbose_name='用例所属模块', to='Square', default=1)
    case_name = models.CharField(verbose_name='用例名称', max_length=32)
    case_prove = models.CharField(verbose_name='Key或者Cookie', max_length=128)
    # 关联到接口表，一对多
    case_api_headers = models.ForeignKey(verbose_name='接口表', to='ApiRequest', default=1)
    case_url = models.CharField(verbose_name='具体的请求URL路径', max_length=128)
    case_parameter = models.CharField(verbose_name='请求参数', max_length=128)
    # 关联到请求方式表，一对多
    case_method_id = models.ForeignKey(verbose_name='请求方式', to='ReqMethod', default=1)
    case_expected_result = models.CharField(verbose_name='预期结果', max_length=128)
    case_actual_results = models.CharField(verbose_name='实际结果', max_length=128)

    class Meta:
        verbose_name_plural = '测试案例表'

    def __str__(self):
        return self.case_name


