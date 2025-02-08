from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from users.serializers import RegisterSerializer, UserSerializer
from users.models import User
from apikeys.models import APIKey
from apikeys.serializers import APIKeySerializer
from postings.models import Posting
import string, secrets
from decimal import Decimal

def generate_random_string(length=12):
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return ''.join(secrets.choice(characters) for _ in range(length))


class UserViewSet(GenericViewSet):
    queryset = User.objects.all()

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

    @action(detail=True, methods=["GET"], url_path="profile")
    def get_user(self, request, pk=None):
        """Retrieve a specific user by ID."""
        try:
            user = self.get_object()
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=["GET"], url_path="pay")
    def pay_user(self, request, *args, **kwargs):
        user = self.get_object()
        posting_id = request.query_params.get("posting_id")
        if not posting_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        posting = Posting.objects.filter(id=posting_id).first()
        if not posting:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # for creators
        if user.user_type == "content_creator":
            user.money_earned += float(posting.price_per_click) * float(posting.percentage_cut)
            user.save()
        elif user.user_type == "developer":
            user.money_earned += float(posting.price_per_click) * (1 - float(posting.percentage_cut))
            user.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET", "DELETE"], url_path="api-keys")
    def api_keys(self, request, *args, **kwargs):
        user = self.get_object()
        is_creating = (request.query_params.get("creating", None) == "true")
        if request.method == "GET":
            if is_creating:
                key = APIKey.objects.create(
                    owner=user,
                    value=generate_random_string()
                )
                serializer = APIKeySerializer(key)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                serializer = APIKeySerializer(user.api_keys.all(), many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "DELETE":
            key_id = request.query_params.get("key_id")
            key = APIKey.objects.filter(id=key_id).first()
            if key:
                key.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
