from django.forms import CharField, ModelForm

from menu.models import MenuItem


class MenuItemAdminForm(ModelForm):
    category = CharField(label='Категория', required=False)

    class Meta:
        model = MenuItem
        fields = '__all__'