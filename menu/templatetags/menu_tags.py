from dataclasses import dataclass
from enum import Enum
from typing import Optional

from django import template
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.utils.safestring import mark_safe

from ..models import MenuItem

register = template.Library()


class Subcategory(Enum):
    ROOT = "root"
    SUB = "sub"
    ITEM = "item"


@dataclass
class Data_:
    menu_name: str
    request: WSGIRequest
    class_: Subcategory = Subcategory.ROOT
    was_active: bool = False
    html: Optional[str] = ''
    all_menu_items: QuerySet = None

    def __post_init__(self):
        self.all_menu_items = MenuItem.objects.filter(menu_name=self.menu_name)


def _recursion(data: Data_, parent_id: int = None) -> Data_:
    menu_items = data.all_menu_items.filter(parent_id=parent_id)
    data.html += '<ul>'

    for item in menu_items:
        is_active = data.request.path == item.get_absolute_url()
        data.class_ = _check_level(item)

        if is_active:
            data.html += _generate_list_item_html(data, item, is_active)
            data.was_active = True
            data = _recursion(data, item.id)
        else:
            data.html += _generate_list_item_html(data, item, is_active)

        if not data.was_active:
            data = _recursion(data, item.id)

    data.html += '</ul>'
    return data


def _generate_list_item_html(data, item, is_active_item) -> str:
    classes = data.class_.value
    if is_active_item:
        classes = " active"

    return mark_safe(
        f'<li><a class="{classes}" href="{item.get_absolute_url()}">{item.name}</a></li>')


def _check_level(item: MenuItem) -> Subcategory:
    if not item.parent:
        return Subcategory.ROOT
    elif not item.parent.parent:
        return Subcategory.SUB
    else:
        return Subcategory.ITEM


@register.simple_tag(takes_context=True)
def draw_menu(context: dict, menu_name: str) -> str:
    data = Data_(
        menu_name=menu_name,
        request=context['request']
    )
    data = _recursion(data)
    return mark_safe(data.html)
