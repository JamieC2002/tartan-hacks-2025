from rest_framework import serializers
from apikeys.models import APIKey

class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = '__all__'
