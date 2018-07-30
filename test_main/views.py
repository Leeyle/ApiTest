from django.shortcuts import render,redirect
from rbac.service.init_permission import init_permission
from test_main import models

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        obj = models.UserMain.objects.filter(username=user, password=pwd).first()
        if obj:
            init_permission(request, obj.auth)
            return redirect('/arya/crm/case/')
        return render(request, 'login.html')
