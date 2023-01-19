from rest_framework import serializers

class BarberRequest(serializers.Serializer):
    """Barber serializer"""
    name = serializers.CharField(max_length = 100)
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    contact_number = serializers.CharField(max_length = 20)