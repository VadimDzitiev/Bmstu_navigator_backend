from .models import Service
from .models import Request
from .models import UserProfile
from .models import RequestService
from rest_framework import serializers


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Service
        # Поля, которые мы сериализуем
        fields = "__all__"

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Request
        # Поля, которые мы сериализуем
        fields = "__all__"
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = UserProfile
        # Поля, которые мы сериализуем
        fields = "__all__"
class RequestServiceSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = RequestService
        # Поля, которые мы сериализуем
        fields = "__all__"