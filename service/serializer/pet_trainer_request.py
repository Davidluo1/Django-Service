from rest_framework import serializers

class PetTrainerRequest(serializers.Serializer):
    """Pet trainer serializer"""
    name = serializers.CharField(max_length = 100)
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    contact_number = serializers.CharField(max_length = 20)