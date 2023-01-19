from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """User input function specification"""
    longitude = models.FloatField(null=False)
    latitude = models.FloatField(null=False)
    email = models.EmailField(max_length=300, unique=True, null=False)
    name = models.CharField(max_length=100, null=False)
    contact_number = models.CharField(max_length=200, null=False)
    otp_verify = models.BooleanField(default=False)