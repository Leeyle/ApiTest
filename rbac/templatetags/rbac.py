from django.template import Library
from django.conf import settings
import re


register = Library()

@register.inclusion_tag('menu_tpl.html')
def menu_html(request):

    permission_menu_list = request.session[settings.OO]
    currnet_url = request.path_info

    page_menu = {}
    for item in permission_menu_list:
        if not item['menu_gp_id']:
            page_menu[item['id']] = item

    for item in permission_menu_list:
        regex = "^{0}$".format(item['url'])
        if re.match(regex, currnet_url):
            menu_gp_id = item['menu_gp_id']
            if menu_gp_id:
                page_menu[menu_gp_id]['active'] = True
            else:
                page_menu[item['id']]['active'] = True
    result = {}
    for item in page_menu.values():
        active = item.get('active')
        menu_id = item['menu_id']
        if menu_id in result:
            result[menu_id]['children'].append({'title':item['title'],'url':item['url'], 'active':active})
            if active:
                result[menu_id]['active'] = True
        else:
            result[menu_id] = {
                'menu_id': item['menu_id'],
                'menu_title': item['menu_title'],
                'active': active,
                'children': [
                    {
                        'title': item['title'],
                        'url': item['url'],
                        'active': active
                    }
                ]
            }
    return {"page_menu": result}



