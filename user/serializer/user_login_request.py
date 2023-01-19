from rest_framework import serializers

class LoginRequest(serializers.Serializer):
    """Login request seralizer"""
    password = serializers.CharField(max_length = 100)
    email = serializers.CharField(max_length = 100)