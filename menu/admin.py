
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest

from .models import MenuItem


class RootFilter(admin.SimpleListFilter):
    title = 'Root Category'
    parameter_name = 'root_cat'

    def lookups(self, request:WSGIRequest, model_admin):
        menu_name = request.GET.get('menu_name')
        # root_cat = request.GET.get('root_cat')
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
            # queryset_filtered = MenuItem.objects.filter(parent_id=parent_id)
            if queryset_filtered:
                return queryset_filtered
        # return queryset

class CategoryFilter(admin.SimpleListFilter):
    title = 'Category'
    parameter_name = 'category'

    def lookups(self, request:WSGIRequest, model_admin):
        menu_name = request.GET.get('menu_name')
        # category = request.GET.get('category')
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
        # root_cat = request.GET.get('root_cat')
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
        # menu_name = request.GET.get('menu_name')
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
    list_filter = (MenuFilter, CategoryFilter)
    search_fields = ('name',)

    def get_list_filter(self, request):
        if 'root_cat' in request.GET:
            return (MenuFilter, RootFilter, CategoryFilter)
        else:
            return (MenuFilter, RootFilter)