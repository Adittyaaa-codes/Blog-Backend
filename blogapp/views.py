from django.shortcuts import render
from rest_framework.views import APIView
from .models import Blog
from .serializers import BlogSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.

class BlogView(APIView):
    authentication_classes = [JWTAuthentication]
    # Remove global permission - handle per method
    def post(self, request):
        # Check authentication for POST requests only
        if not request.user or not request.user.is_authenticated:
            return Response({'error': 'Authentication required to create posts.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            data = request.data
            serializer = BlogSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request, pk=None):
        try:
            if pk:
                # Get individual blog by UUID
                try:
                    blog = Blog.objects.get(pk=pk)
                    serializer = BlogSerializer(blog, context={'request': request})
                    return Response(serializer.data)
                except Blog.DoesNotExist:
                    return Response({'error': 'Blog not found.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                # Get all blogs
                blogs = Blog.objects.all()
                serializer = BlogSerializer(blogs, many=True, context={'request': request})
                return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def patch(self, request, pk=None):
        try:
            if pk is None:
                return Response({'error': 'Blog ID required.'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                blog = Blog.objects.get(pk=pk)
            except Blog.DoesNotExist:
                return Response({'error': 'Blog not found.'}, status=status.HTTP_404_NOT_FOUND)
            if blog.user != request.user:
                return Response({'error': 'You can only edit your own blog.'}, status=status.HTTP_403_FORBIDDEN)
            serializer = BlogSerializer(blog, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk=None):
        try:
            if pk is None:
                return Response({'error': 'Blog ID required.'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                blog = Blog.objects.get(pk=pk)
            except Blog.DoesNotExist:
                return Response({'error': 'Blog not found.'}, status=status.HTTP_404_NOT_FOUND)
            if blog.user != request.user:
                return Response({'error': 'You can only delete your own blog.'}, status=status.HTTP_403_FORBIDDEN)
            blog.delete()
            return Response({'message': 'Blog deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
