from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from postings.models import Posting
from postings.serializers import PostingSerializer, ShowPostingSerializer
from users.models import User

class PostingViewSet(viewsets.ModelViewSet):
    """Handles CRUD operations for postings"""
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get("user_id")
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user_postings = ShowPostingSerializer(user.postings.all(), many=True)
        return Response(user_postings.data, status=status.HTTP_200_OK)

    # @action(detail=False, methods=['post'])
    # def get_ads(self, request, pk=None):
