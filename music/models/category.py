from django.db import models
from .base import ModelBase


class Category(ModelBase):
    class Meta:
        verbose_name = "Category"

    title = models.CharField(max_length=100)
