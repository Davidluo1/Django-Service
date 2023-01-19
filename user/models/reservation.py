from django.db import models

class Reservation(models.Model):
    """Reservation model specification"""
    user = models.ForeignKey("user.User", models.DO_NOTHING)
    service_name = models.CharField(max_length=200)
    shift = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)