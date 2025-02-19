from rest_framework import serializers
from .models import EmainVerificationToken
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class Registerserializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'password2')
        extra_kwargs = {
            'first_name':{'required':True},
            'last_name':{'required':True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "password fieids didn't match! "})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['last_name'],
            last_name = validated_data['last_name'],
            is_active = False
        )
        user.set_password(validated_data['password'])
        user.save()

        token = EmainVerificationToken.objects.create(user=user)

        verification_link = f"http://127.0.0.1:8000/api/verify-email/{token.token}/"
        send_mail(
            'verify your Email',
            f'please click the link to verify your email: {verification_link}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        return user
    

class Loginserializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            # print(user)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('User account is disabled')
                
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError('Invalid credentials.')
            
        else:
            raise serializers.ValidationError('Both username and password is required')


from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'id': {'read_only': True}, 
            'username': {'read_only': True},  
        }

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance