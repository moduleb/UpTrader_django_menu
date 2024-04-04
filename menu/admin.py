
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest

from .models import MenuItem


class ParentFilter(admin.SimpleListFilter):
    title = 'parent'
    parameter_name = 'parent__id'

    def lookups(self, request:WSGIRequest, model_admin):
        parent_id = request.GET.get('parent__id')
        items = MenuItem.objects.filter(parent_id=parent_id)

        if not items:
            item = MenuItem.objects.filter(id=parent_id)
            for i in items:
                items = MenuItem.objects.filter(parent=i.parent_id)

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
            else:
                return queryset
        return queryset



@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'url', 'named_url')
    list_filter = (ParentFilter,)
    # list_filter = ('parent',)
    search_fields = ('name',)
