from .models import *
from rest_framework import serializers
from collections import OrderedDict


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Service
        # Поля, которые мы сериализуем
        fields = "__all__"


class UserAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email']


class RequestSerializer(serializers.ModelSerializer):
    user = UserAppSerializer(read_only=True)

    class Meta:
        # Модель, которую мы сериализуем
        model = Request
        # Поля, которые мы сериализуем
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    is_moderator = serializers.BooleanField(default=False, required=False)

    class Meta:
        model = Users
        fields = ['email', 'password', 'is_moderator']


class RequestServiceSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = RequestService
        # Поля, которые мы сериализуем
        fields = "__all__"
