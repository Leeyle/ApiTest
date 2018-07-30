# -*- coding:utf-8 -*-
# /user/bin/python
# @Time   : 2018/7/21 15:16
# @Author : liyongle
# @File   : warrior.py

from django.shortcuts import HttpResponse, render, redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.forms import ModelForm
from arya.utils.page import Pagination
import copy

class ChangeList(object):
    """
    专门处理页面所有内容
    """
    def __init__(self, config, queryset):

        self.config = config
        self.q_value = config.request.GET.get('q','')
        self.list_display = config.list_display()
        self.show_add = config.show_add()
        self.add_url = config.reverse_add_url()
        self.search_list = config.get_search_list()
        self.actions = config.get_actions()

        # 处理分页数据
        request = config.request
        query_params = copy.deepcopy(request.GET)  # QueryDict
        current_page = request.GET.get('page', 1)
        per_page = config.per_page
        pager_page_count = config.pager_page_count
        all_count = queryset.count()
        base_url = config.reverse_list_url()
        page_obj = Pagination(current_page, all_count, base_url, query_params, per_page, pager_page_count)
        self.queryset = queryset[page_obj.start:page_obj.end]
        self.page_html = page_obj.page_html()

        def table_header(self):
            data = []
            for str_func in self.list_display:
                if isinstance(str_func, str):
                    val = self.config.model_class._meta.get_field(str_func).verbose_name
                else:
                    val = str_func(self.config, is_header=True)
                data.append(val)
            return data

        def table_body(self):
            table_data = []
            for obj in self.queryset:
                row = []
                for str_func in self.list_display:
                    if isinstance(str_func, str):
                        col = getattr(obj, str_func)
                    else:
                        col = str_func(self.config, obj)
                    row.append(col)
                table_data.append(row)

            return table_data

        def action_options(self):
            data = []
            for func in self.actions:
                temp = {'value': func.__name__, 'text': func.text}
                data.append(temp)
            return data

class AryaConfig(object):

    # 1. 列表显示列相关
    list_display = []

    def get_list_display(self):
        result = []
        result.extend(self.list_display)
        # 如果有编辑权限
        result.append(AryaConfig.row_edit)
        # 如果有删除权限
        result.append(AryaConfig.row_del)
        result.insert(0,AryaConfig.row_checkbox)
        return result

    def row_del(self,row=None,is_header=None):
        if is_header:
            return '删除'
        # return row.name + row.email+str(row.id)
        # 生成删除URL
        # app01_userinfo_delete
        app = self.model_class._meta.app_label
        md = self.model_class._meta.model_name
        name = "arya:%s_%s_delete" %(app,md,) # arya:app01_userinfo_delete
        url = reverse(viewname=name,args=(row.id,))
        return mark_safe("<a href='{0}'>删除</a>".format(url))

    def row_edit(self,row=None,is_header=None):
        if is_header:
            return '编辑'
        # return row.name + row.email+str(row.id)
        # 生成删除URL
        # app01_userinfo_delete
            app = self.model_class._meta.app_label
        md = self.model_class._meta.model_name
        name = "arya:%s_%s_change" %(app,md,) # arya:app01_userinfo_delete
        url = reverse(viewname=name,args=(row.id,))
        return mark_safe("<a href='{0}'>编辑</a>".format(url))

    def row_checkbox(self,row=None,is_header=None):
        if is_header:
            return '选择'
        return mark_safe("<input type='checkbox' name='pk' value='{0}' />".format(row.id))

    # 2. 添加按钮相关
    show_add = True
    def get_show_add(self):
        # 如果有增加权限，否则返回False
        return self.show_add

    # 3. ModelForm
    model_form_class = None
    def get_model_form_class(self):
        if self.model_form_class:
            return self.model_form_class

        class DynamicModelForm(ModelForm):
            class Meta:
                model = self.model_class
                fields = "__all__"

        return DynamicModelForm

    # 4. 模糊搜索
    search_list = []

    def get_search_list(self):
        rest = []
        rest.extend(self.search_list)
        return rest

    # 5. 分页配置
    # 每页显示10条数据
    per_page = 10
    # 页面上最多显示的页面个数
    pager_page_count = 11

    # 6. Action
    actions = []
    def get_actions(self):
        result = []
        result.extend(self.actions)
        return result

    def __init__(self,model_class,site):
        self.model_class = model_class
        self.site = site
    @property
    def urls(self):
        from django.conf.urls import url, include
        #self.model_class # UserInfo,UserGroup
        app = self.model_class._meta.app_label
        md = self.model_class._meta.model_name
        partterns = [
            url(r'^$', self.changelist_view,name="%s_%s_list" %(app,md,)),
            url(r'^add/', self.add_view,name="%s_%s_add" %(app,md,)),
            url(r'^(\d+)/change/', self.change_view,name="%s_%s_change" %(app,md,)),
            url(r'^(\d+)/delete/', self.delete_view,name="%s_%s_delete" %(app,md,)),
        ]
        partterns += self.extra_url()
        return partterns

    def extra_url(self):
        return []

    def reverse_add_url(self):
        app = self.model_class._meta.app_label
        md = self.model_class._meta.model_name
        name = "arya:%s_%s_add" % (app, md,)  # arya:app01_userinfo_delete
        url = reverse(viewname=name)
        return url

    def reverse_list_url(self):
        app = self.model_class._meta.app_label
        md = self.model_class._meta.model_name
        name = "arya:%s_%s_list" % (app, md,)  # arya:app01_userinfo_delete
        url = reverse(viewname=name)
        return url

    def changelist_view(self,request):

        # UserInfoConfig对象 =  self
        # UserTypeConfig对象 =  self
        self.request = request
        if request.method == "POST":
            action_item_name = request.POST.get('select_ac') # multi_init /multi_delete
            if action_item_name:
                func = getattr(self,action_item_name)
                func(request)
        from django.db.models import Q
        condition = Q()
        search_q = request.GET.get('q')
        search_list = self.get_search_list() # [name__contains,pwd]
        if search_q and search_list:
            for field in search_list:
                temp = Q()
                convert_type = field.get('type')
                if convert_type:
                    try:
                        search_q = convert_type(search_q)
                    except Exception as e:
                        continue
                temp.children.append((field.get('k'),search_q))
                condition.add(temp,'OR')

        queryset = self.model_class.objects.filter(condition)
        cl = ChangeList(self,queryset)
        return render(request,'arya/changelist.html',{'cl':cl})

    def add_view(self,request):
        self.request = request
        # self.model_class/ userinfo
        # self.model_class/ usertype
        model_form_cls = self.get_model_form_class()
        if request.method == "GET":
            form = model_form_cls()
            return render(request,'arya/add_view.html',{'form':form})
        else:
            form = model_form_cls(data=request.POST)
            if form.is_valid():
                form.save()
                # 反向生成URL，跳转回列表页面
                return redirect(self.reverse_list_url())
            return render(request, 'arya/add_view.html', {'form': form})

    def change_view(self,request,nid):
        self.request = request
        obj = self.model_class.objects.filter(pk=nid).first()
        if not obj:
            return redirect(self.reverse_list_url())

        model_form_cls = self.get_model_form_class()
        if request.method == 'GET':
            # 在Input框中显示默认值
            form = model_form_cls(instance=obj)
            return render(request,'arya/change_view.html',{'form':form})
        else:
            form = model_form_cls(instance=obj,data=request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.reverse_list_url())
            return render(request, 'arya/change_view.html', {'form': form})

    def delete_view(self,request,nid):
        self.request = request
        obj = self.model_class.objects.filter(id=nid).first()
        if not obj:
            return redirect(self.reverse_list_url())
        if request.method == "GET":
            return render(request,'arya/delete_view.html')
        else:
            obj.delete()
            return redirect(self.reverse_list_url())

class AryaSite(object):
    def __init__(self):
        self._registry = {}

    def register(self,class_name,config_class):
        """
        self._registry = {
            models.UserInfo: obj1 = AryaConfig(models.UserInfo,site),
            models.UserType: obj2 = AryaConfig(models.UserType,site),
        }
        :param class_name:
        :param config_class:
        :return:
        """
        self._registry[class_name] = config_class(class_name,self)
    @property
    def urls(self):
        from django.conf.urls import url, include
        partterns = [
            url(r'^login/', self.login),
            url(r'^logout/', self.logout),
        ]

        for model_class,arya_config_obj in self._registry.items():
            #print(model_class,arya_config_obj,   model_class._meta.app_label,model_class._meta.model_name,)
            # /app01/userinfo/
            # /app01/usertype/
            app_model_name = r'^{0}/{1}/'.format(model_class._meta.app_label,model_class._meta.model_name)
            pt = url(app_model_name, (arya_config_obj.urls,None,None))
            partterns.append(pt)

        return partterns

    def login(self,request):
        from django.shortcuts import HttpResponse
        return HttpResponse('Login')

    def logout(self,request):
        from django.shortcuts import HttpResponse
        return HttpResponse('Logout')

site = AryaSite()
