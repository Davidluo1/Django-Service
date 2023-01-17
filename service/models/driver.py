from django.db import models

class Driver(models.Model):
    #user = models.ForeignKey("user.User", models.DO_NOTHING)
    name = models.CharField(max_length=200)
    longitude = models.FloatField(null=False)
    latitude = models.FloatField(null=False)
    morning_shift = models.BooleanField(default=False)
    afternoon_shift = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)