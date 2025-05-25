from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .models import UserModel
from .serializers import UserModelSerializer
# Create your views here.

class UserModelView(CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [AllowAny]

