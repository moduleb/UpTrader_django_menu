from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest

from menu.models import MenuItem


class RootFilter(admin.SimpleListFilter):
    title = 'Root Category'
    parameter_name = 'root_cat'

    def lookups(self, request:WSGIRequest, model_admin):
        menu_name = request.GET.get('menu_name')
        if menu_name:
            items = MenuItem.objects.filter(parent__isnull=True, menu_name=menu_name)
        else:
            items = MenuItem.objects.filter(parent__isnull=True)

        r_ = ()
        for item in items:
            r_ += ((item.id, item.name),)
        return r_

    def queryset(self, request, queryset):
        parent_id = self.value()
        if parent_id:
            queryset_filtered = queryset.filter(parent_id=parent_id)
            if queryset_filtered:
                return queryset_filtered

class CategoryFilter(admin.SimpleListFilter):
    title = 'Category'
    parameter_name = 'sub_cat'

    def lookups(self, request:WSGIRequest, model_admin):
        menu_name = request.GET.get('menu_name')
        root_cat = request.GET.get('root_cat')
        if menu_name:
            items = MenuItem.objects.filter(parent=root_cat, menu_name=menu_name)
        else:
            items = MenuItem.objects.filter(parent=root_cat)

        r_ = ()
        for item in items:
            r_ += ((item.id, item.name),)
        return r_

    def queryset(self, request, queryset):
        category = self.value()
        if category:
            item = queryset.filter(id = category).first()
            if item:
                queryset_filtered = MenuItem.objects.filter(parent_id=category)
                return queryset_filtered
            else:
                return queryset


class MenuFilter(admin.SimpleListFilter):
    title = 'Menu Name'
    parameter_name = 'menu_name'

    def lookups(self, request:WSGIRequest, model_admin):
        items = MenuItem.objects.values_list('menu_name', flat=True).distinct()

        r_ = ()
        for item in items:
            r_ += ((item, item),)
        return r_

    def queryset(self, request, queryset):
        menu_name = self.value()
        if menu_name:
            queryset_filtered = queryset.filter(menu_name=menu_name)
            if queryset_filtered:
                return queryset_filtered
        return queryset


"""
class BaseListFilter(admin.SimpleListFilter):
    def get_items(self, request: WSGIRequest, **kwargs):
        menu_name = request.GET.get('menu_name')
        if menu_name:
            items = MenuItem.objects.filter(**kwargs, menu_name=menu_name)
        else:
            items = MenuItem.objects.filter(**kwargs)
        return items

    def lookups(self, request: WSGIRequest, model_admin):
        items = self.get_items(request, **self.filter_kwargs)
        r_ = ()
        for item in items:
            r_ += ((item.id, item.name),)
        return r_

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            queryset_filtered = queryset.filter(**self.queryset_filter_kwargs(value))
            if queryset_filtered:
                return queryset_filtered
        return queryset

    def queryset_filter_kwargs(self, value):
        raise NotImplementedError("Subclasses must implement this method.")

class RootFilter(BaseListFilter):
    title = 'Root Category'
    parameter_name = 'root_cat'
    filter_kwargs = {'parent__isnull': True}

    def queryset_filter_kwargs(self, value):
        return {'parent_id': value}

class CategoryFilter(BaseListFilter):
    title = 'Category'
    parameter_name = 'category'
    filter_kwargs = {'parent__isnull': False}

    def queryset_filter_kwargs(self, value):
        return {'parent_id': value}

class MenuFilter(BaseListFilter):
    title = 'Menu Name'
    parameter_name = 'menu_name'
    filter_kwargs = {}

    def lookups(self, request: WSGIRequest, model_admin):
        items = MenuItem.objects.values_list('menu_name', flat=True).distinct()
        r_ = ()
        for item in items:
            r_ += ((item, item),)
        return r_

    def queryset_filter_kwargs(self, value):
        return {'menu_name': value}

"""