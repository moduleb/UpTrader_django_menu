
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest

from .models import MenuItem


class AnimalFilter(admin.SimpleListFilter):
    title = 'Animal'
    parameter_name = 'parent_id'

    def lookups(self, request:WSGIRequest, model_admin):
        parent_id = request.GET.get('parent_id')
        items = MenuItem.objects.filter(parent_id=parent_id)

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
        return queryset


class MenuFilter(admin.SimpleListFilter):
    title = 'Menu Name'
    parameter_name = 'menu_name'

    def lookups(self, request:WSGIRequest, model_admin):
        menu_name = request.GET.get('menu_name')
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


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'url', 'named_url')
    list_filter = (MenuFilter, AnimalFilter,)
    # list_filter = ('parent',)
    search_fields = ('name',)

