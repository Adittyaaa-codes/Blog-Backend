from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    confirm_password = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists")
        return data 
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['name']  # or split into first_name/last_name if needed
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class LoginSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    