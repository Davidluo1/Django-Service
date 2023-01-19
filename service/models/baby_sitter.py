from django.db import models

class BabySitter(models.Model):
    """Baby sitter model specification"""
    #user = models.ForeignKey("user.User", models.DO_NOTHING)
    name = models.CharField(max_length=200)
    longitude = models.FloatField(null=False)
    latitude = models.FloatField(null=False)
    morning_shift = models.BooleanField(default=False)
    afternoon_shift = models.BooleanField(default=False)
    # contact_number = models.CharField(max_length=10)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)