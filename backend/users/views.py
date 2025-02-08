from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from users.serializers import RegisterSerializer, UserSerializer
from users.models import User


class UserViewSet(GenericViewSet):
    @action(detail=False, methods=["POST"], url_path="register")
    def register(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"], url_path="login")
    def login(self, request, *args, **kwargs):
        user = User.objects.filter(
            email=request.data["email"],
            password=request.data["password"]
        ).first()
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
