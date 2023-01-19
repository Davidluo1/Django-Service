from rest_framework import serializers
from django.core.validators import MaxValueValidator, MinValueValidator

class SignUpRequest(serializers.Serializer):
    """Sign up request seralizer"""
    name = serializers.CharField(max_length = 100)
    email = serializers.CharField(max_length = 100)
    password = serializers.CharField(max_length = 100)
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    contact_number = serializers.CharField(max_length = 20)
    username = serializers.CharField(max_length = 100)