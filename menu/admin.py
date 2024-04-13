from dataclasses import dataclass

from django.contrib import admin
from django.db.models import QuerySet
from django.forms import ModelChoiceField, CharField, HiddenInput, ChoiceField, ModelForm

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
        filters = (MenuFilter, RootFilter)
        root_cat = request.GET.get('root_cat', None)
        if root_cat:
            has_children = MenuItem.objects.filter(id=root_cat).first().children.exists()
            if has_children:
                filters = (MenuFilter, RootFilter, CategoryFilter)
        return filters

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        filters = request.session.get('admin_filters', '')
        menu_name = filters.get('menu_name')
        root_cat = filters.get('root_cat')
        sub_cat = filters.get('sub_cat')

        if menu_name:
            queryset = MenuItem.objects.filter(menu_name=menu_name)
        else:
            queryset = MenuItem.objects.all()

        if not menu_name and root_cat:
            menu_name = queryset.filter(id=root_cat).first().menu_name
            queryset = queryset.filter(menu_name=menu_name)

        data = Data_(
            form=form,
            queryset=queryset,
            menu_name=menu_name,
            root_cat=root_cat,
            sub_cat=sub_cat
        )

        if root_cat and sub_cat:
            _show_menu_name(data)
            _show_category(data, disabled=True)
            _set_parent(data, init=True, required=True)

        elif root_cat:
            _show_menu_name(data)
            _hide_category(data)
            _set_parent(data, label="Category", root_query=True, required=True, init=True)

        elif menu_name and not root_cat:
            _show_menu_name(data)
            _hide_category(data)
            _set_parent(data, label="Category", root_query=True)

        elif not menu_name:
            _create_new_menu_name(data)
            _hide_category(data)
            _set_parent(data, label="Category", disabled=True)

        order = ['name', "url", "named_url", 'menu_name', 'category', "parent"]
        data.form.base_fields = {k: data.form.base_fields[k] for k in order}

        return data.form


@dataclass
class Data_:
    form: ModelForm
    queryset: QuerySet
    menu_name: str = None
    root_cat: int = None
    sub_cat: int = None


def _create_new_menu_name(data):
    data.form.base_fields['menu_name'] = CharField(required=True, label="Menu Name")


def _set_parent(data: Data_, required=False, disabled=False, label="Subcategory", root_query=False, init=None) -> None:
    if root_query:
        queryset = data.queryset.filter(parent_id=None)
    else:
        if data.root_cat:
            queryset = data.queryset.filter(parent_id=data.root_cat)
        else:
            queryset = data.queryset

    if init:
        if root_query:
            init = data.root_cat
        elif data.sub_cat:
            init = data.sub_cat
        else:
            init = queryset.first().id

    data.form.base_fields['parent'] = ModelChoiceField(
        queryset=queryset,
        label=label,
        required=required,
        disabled=disabled,
        initial=init
    )


def _show_category(data: Data_, disabled=False) -> None:
    data.form.base_fields['category'] = ModelChoiceField(
        queryset=data.queryset,
        label="Category",
        required=False,
        disabled=disabled,
        initial=data.root_cat,
    )


def _hide_category(data):
    data.form.base_fields['category'] = CharField(required=False, widget=HiddenInput())


def _hide_parent(data):
    data.form.base_fields['parent'] = CharField(required=False, widget=HiddenInput())


def _show_menu_name(data: Data_) -> None:
    data.form.base_fields['menu_name'] = ChoiceField(
        choices=[(data.menu_name, data.menu_name)],
        required=True,
        label='Menu Name',
        initial=data.menu_name,
        disabled=True
    )
