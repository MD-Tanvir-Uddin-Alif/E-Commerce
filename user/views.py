from django.shortcuts import render, get_object_or_404
from .models import EmainVerificationToken
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from .serializers import Registerserializer, Loginserializer, UserSerializer
# Create your views here.


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = Registerserializer


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, token):
        verification_token = get_object_or_404(EmainVerificationToken, token=token)

        user = verification_token.user
        user.is_active = True
        user.save()

        verification_token.delete()

        return Response({'detail': 'Email verified sucessfully. You can now log in.'}, status=status.HTTP_200_OK)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = Loginserializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            # print(user, token)
            return Response({'token': token.key}, status=200)
        else:
            return Response(serializer.errors, status=400)
        

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        print('logouted')
        return Response({'detail': 'Successfully logged out'}, status=200)
    


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        print(serializer.data)
        return Response(serializer.data, status=200)
    
import logging

logger = logging.getLogger(__name__)

class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        logger.debug(f"User: {request.user}, Token: {request.auth}")
        serializer = UserSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)