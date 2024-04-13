from django.db import models


class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    url = models.CharField(max_length=200)
    menu_name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
