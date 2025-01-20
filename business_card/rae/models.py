from django.contrib.auth.models import AbstractUser
from django.db import models


class BusinessCard(AbstractUser):
    name = models.CharField(max_length=128)
    company = models.CharField(max_length=128)
    phone = models.CharField(max_length=32)
    photo = models.ImageField(upload_to="photos/", blank=True)
    url = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.name}: {self.company}"
