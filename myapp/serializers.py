from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'password',
                  'password2', 'email', 'name', 'photo')
        extra_kwargs = {
            'name': {'required': True},
            'email': {'required': True},
            'photo': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
            name=validated_data['name'],
            photo=validated_data['photo'] if 'photo' in validated_data else None,
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=15)

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'password')
