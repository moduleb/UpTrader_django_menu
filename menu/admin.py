from django.contrib import admin
from django.forms import ModelChoiceField, CharField, ModelMultipleChoiceField, \
    RadioSelect, TextInput, HiddenInput

from menu.admin_addons.filters import MenuFilter, CategoryFilter, RootFilter
from menu.admin_addons.form import MenuItemAdminForm
from menu.models import MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'url', 'named_url')
    search_fields = ('name',)
    form = MenuItemAdminForm

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Сохраняем текущие параметры фильтрации в сессии
        request.session['admin_filters'] = request.GET.copy()
        return queryset

    def get_list_filter(self, request):
        # Показываем фильтр подкатегорий если выбрана основная категория
        if 'root_cat' in request.GET:
            return (MenuFilter, RootFilter, CategoryFilter)
        else:
            return (MenuFilter, RootFilter)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        filters = request.session.get('admin_filters', '')
        menu_name = filters.get('menu_name', '')
        root_cat = filters.get('root_cat', None)
        sub_cat = filters.get('sub_cat', '')

        # Скрываем поле url
        form.base_fields['url'] = CharField(widget=HiddenInput())

        item = MenuItem.objects.filter(id=root_cat).first()

        if root_cat:
            label = "SubCategory:"
            menu_name = item.menu_name
            form.base_fields['category'] = CharField(
                label="Category",
                initial=item.name,
                widget=TextInput(attrs={'readonly': 'readonly'})
            )
        else:
            form.base_fields['category'] = CharField(widget=HiddenInput())
            label = "Category:"


        if menu_name:
            queryset = MenuItem.objects.filter(parent_id=root_cat, menu_name=menu_name)
        else:
            queryset = MenuItem.objects.filter(parent_id=root_cat)

        if not menu_name:
            form.base_fields['menu_name'] = ModelChoiceField(
                queryset=MenuItem.objects.values_list('menu_name', flat=True).distinct(),
                required=True,
                label='Menu Name',
            )

        else:
            form.base_fields['menu_name'] = CharField(
                initial=menu_name,
                label="Menu Name",
                widget=TextInput(attrs={'readonly': 'readonly'})
            )

        form.base_fields['parent'] = ModelChoiceField(
            queryset=queryset,
            required=False,
            label=label,
        )

        order = ['name', "named_url", 'menu_name', "category", 'parent']
        form.base_fields = {k: form.base_fields[k] for k in order}

        return form
