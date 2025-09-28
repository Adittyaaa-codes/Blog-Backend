from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response    
from .serializers import RegisterSerializers, LoginSerializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class LoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializers(data=data)
            if serializer.is_valid():
                username = serializer.validated_data.get('username')
                password = serializer.validated_data.get('password')
                
                user = authenticate(username=username, password=password)
                if user is None:
                    return Response({"error": "Invalid credentials"}, status=400)

                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                })

        except Exception as e:
            return Response({"error": str(e)})

        return Response(serializer.errors)

class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = RegisterSerializers(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User registered successfully"})
        except Exception as e:
            return Response({"error": str(e)})

        return Response(serializer.errors)


class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            return Response({
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)