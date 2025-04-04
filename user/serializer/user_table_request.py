from rest_framework import serializers
from user.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Table password encryption seralizer"""
    @classmethod
    def create(self, validated_data):
        # Pop off the password in database
        password = validated_data.pop("password")
        # Create a user class to store the rest-data
        instance = self.Meta.model(**validated_data)
        # Encrypt password
        instance.set_password(password)
        # Save data
        instance.save()
        return instance
    
    class Meta:
        model = User
