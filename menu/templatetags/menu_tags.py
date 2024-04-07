from django import template
from django.core.handlers.wsgi import WSGIRequest
from django.utils.safestring import mark_safe
from ..models import MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name, parent_id=None):
    request: WSGIRequest = context['request']

    menu_items = MenuItem.objects.filter(parent_id=parent_id, menu_name=menu_name)

    html = '<ul>'
    for item in menu_items:

        is_active = False

        if request.path == item.get_absolute_url():
            is_active = True

        is_active_category = False

        animal = context.get('animal')
        if animal and item.url:
            if item.url in  request.path:
                is_active_category = True

        if is_active:
            html += '<li><a style="color: green;" href="{}">{}</a>'.format(item.get_absolute_url(), item.name)
        else:
            html += '<li><a href="{}">{}</a>'.format(item.get_absolute_url(), item.name)

        if item.children.exists() and is_active_category:
            # Рекурсивно вызываем draw_menu для дочерних элементов, передавая идентификатор текущего элемента
            html += draw_menu(context, menu_name, item.id)
        html += '</li>'
    html += '</ul>'
    return mark_safe(html)


