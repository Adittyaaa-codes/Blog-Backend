from rest_framework import serializers
from .models import Blog
from django.contrib.auth.models import User

class BlogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    uploaded_at = serializers.DateTimeField(source='created_at', read_only=True)
    
    class Meta:
        model = Blog
        fields = ['uid', 'blog', 'caption', 'post', 'user_name', 'uploaded_at']
    
    def create(self, validated_data):
        # Set the user to the authenticated user making the request
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)