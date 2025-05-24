from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserModel


class UserModelSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    password = serializers.CharField()
    
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'username', 'email','phone_number','password']
    
    def create(self, validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        username = validated_data['username']
        email = validated_data['username']
        phone_number = validated_data['phone_number']
        password = validated_data['password']
        
        user = User.objects.create_user(
            first_name = first_name,
            last_name =last_name,
            username=username,
            email=email,
            password=password
        )
        
        user_model = UserModel.objects.create(
            user = user,
            phone_number = phone_number
        )
        
        return user_model