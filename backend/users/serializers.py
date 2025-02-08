from rest_framework import serializers
from users.models import User
from apikeys.serializers import APIKeySerializer

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, allow_null=False, allow_blank=False, write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "user_type"
        ]

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("An account with this username already exists.")
        return username
    
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return email

class UserSerializer(serializers.ModelSerializer):
    api_keys = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "user_type",
            "money_earned",
            "api_keys",
            "brand_budget"
        ]

    def get_api_keys(self, obj):
        if obj.user_type == "developer":
            serializer = APIKeySerializer(obj.api_keys.all(), many=True)
            return serializer.data
        return []