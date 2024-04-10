from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    url = models.CharField(max_length=200, null=True, blank=True)
    named_url = models.CharField(max_length=200, null=True, blank=True)
    menu_name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def clean(self):
        if not self.url and not self.named_url:
            raise ValidationError("Оба поля url и named_url не могут быть пустыми одновременно.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
