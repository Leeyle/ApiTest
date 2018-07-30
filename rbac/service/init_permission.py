# -*- coding:utf-8 -*-
# /user/bin/python

from django.conf import settings

def init_permission(request, username):
    """
    用户权限信息初始化，获取当前用户所有权限信息，并保存到Session中
    :param request:
    :param username:
    :return:
    """
    print(username)
    permission_list = username.user_role.filter(permissions__id__isnull=False).values(
        "permissions__id",
        "permissions__title",
        "permissions__url",
        "permissions__code",
        "permissions__group",
        "permissions__menu_gp_id",          # 组内菜单ID，Null表示是菜单
        "permissions__group_id",            # 权限的组ID
        "permissions__group__menu_id",      # 权限的组的菜单ID
        "permissions__group__menu__title"    # 权限的组的菜单名称
    ).distinct()
    print(permission_list)

    # 菜单相关
    permission_menu_list = []
    for item in permission_list:
        # is_menu = item["permissions__is_menu"]
        # if not is_menu:
        #     continue
        temp = {
            "id": item["permissions__id"],
           "title": item["permissions__title"],
           "url": item["permissions__url"],
           "menu_gp_id": item["permissions__menu_gp_id"],
           "menu_id": item["permissions__group__menu_id"],
           "menu_title": item["permissions__group__menu__title"],
        }
        print(temp)
        permission_menu_list.append(temp)
        request.session[settings.OO] = permission_menu_list

    # 权限相关
    permission_dict = {}
    for item in permission_list:
        group_id = item["permissions__group_id"]
        code = item["permissions__code"]
        url = item["permissions__url"]
        if group_id in permission_dict:
            permission_dict[group_id]["codes"].append(code)
            permission_dict[group_id]["urls"].append(url)
        else:
            permission_dict[group_id] = {
                "codes":[code, ],
                "urls":[url, ]
            }
    request.session[settings.XX] = permission_dict