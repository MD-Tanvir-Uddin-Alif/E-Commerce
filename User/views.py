from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .models import UserModel
from .serializers import UserModelSerializer
# Create your views here.

class UserModelView(CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer


