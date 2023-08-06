from django.db import models


class Reader(models.Model):
    name = models.CharField(max_length=300)
    street = models.TextField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=40, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name
