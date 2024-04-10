from dataclasses import dataclass
from enum import Enum
from typing import Optional

from django import template
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.utils.safestring import mark_safe

from ..models import MenuItem

register = template.Library()


class ClassEnum(Enum):
    ROOT = "root"
    SUB = "sub"
    ITEM = "item"
    ACTIVE = "active"


@dataclass
class Data_:
    menu_name: str
    request: WSGIRequest
    was_active: bool = False
    html: Optional[str] = ''
    all_menu_items: QuerySet = None

    def __post_init__(self):
        self.all_menu_items = MenuItem.objects.filter(menu_name=self.menu_name)


def _recursion(data: Data_, parent_id: int = None) -> Data_:
    menu_items = data.all_menu_items.filter(parent_id=parent_id)
    data.html += '<ul>'

    for item in menu_items:

        # Сворачиваем меню при запросе без параметров
        if data.request.path == '/':
            data.was_active = True

        is_active_item = data.request.path == item.get_absolute_url()
        is_active_category = item.get_absolute_url() in data.request.path

        if is_active_item:
            data.html += _generate_list_item_html(item, is_active_item)
            data.was_active = True
            if item.children.exists():
                data = _recursion(data, item.id)
        else:
            data.html += _generate_list_item_html(item, is_active_category)

        if not data.was_active and item.children.exists():
            data = _recursion(data, item.id)

    data.html += '</ul>'
    return data


def _generate_list_item_html(item, is_active_item) -> str:
    classes: str = _check_level(item).value

    if is_active_item:
        classes += " " + ClassEnum.ACTIVE.value

    return mark_safe(
        f'<li><a class="{classes}" href="{item.get_absolute_url()}">{item.name}</a></li>')


def _check_level(item: MenuItem) -> ClassEnum:
    if not item.parent:
        return ClassEnum.ROOT
    elif not item.parent.parent:
        return ClassEnum.SUB
    else:
        return ClassEnum.ITEM


@register.simple_tag(takes_context=True)
def draw_menu(context: dict, menu_name: str) -> str:
    data = Data_(
        menu_name=menu_name,
        request=context['request']
    )
    data = _recursion(data)
    return mark_safe(data.html)
