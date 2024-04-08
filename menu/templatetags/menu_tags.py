from django import template
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.utils.safestring import mark_safe
from ..models import MenuItem

register = template.Library()

def _recursion(all_menu_items, request, parent_id=None, was_active=False):
    """
    Рекурсивно строит HTML для меню, учитывая активные элементы.

    :param all_menu_items: QuerySet всех элементов меню
    :param request: request текущего запроса
    :param parent_id: ID родительского элемента меню, по умолчанию None
    :param was_active: Флаг, указывающий, был ли выведен активный пункт меню, по умолчанию False
    :return: was_active, html - флаг активности и сгенерированный HTML
    """
    menu_items = all_menu_items.filter(parent_id=parent_id)
    html = '<ul class="menu">'
    for item in menu_items:
        if request.path == item.get_absolute_url():
            html += f'<li><a class="active" href="{item.get_absolute_url()}">{item.name}</a>'
            was_active = True
            if item.children.exists():
                was_active, html_new = _recursion(all_menu_items, request, item.id, was_active)
                html += html_new
        else:
            html += f'<li><a href="{item.get_absolute_url()}">{item.name}</a>'

        if item.children.exists() and not was_active:
            was_active, html_new = _recursion(all_menu_items, request, item.id, was_active)
            html += html_new

        html += '</li>'
    html += '</ul>'
    return was_active, mark_safe(html)

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request: WSGIRequest = context['request']
    all_menu_items: QuerySet = MenuItem.objects.filter(menu_name=menu_name)
    _, html = _recursion(all_menu_items, request)
    return html


