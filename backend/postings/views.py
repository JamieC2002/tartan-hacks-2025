from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from postings.models import Posting
from postings.serializers import PostingSerializer, ShowPostingSerializer, PostingSubmissionsSerializer, ContentCreatorPostingSerializer
from users.models import User
from django.shortcuts import get_object_or_404

class PostingViewSet(viewsets.ModelViewSet):
    """Handles CRUD operations for postings"""
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get("user_id", None)
        
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if user.user_type == "brand":
            user_postings = ShowPostingSerializer(user.postings.all(), many=True)
            return Response(user_postings.data, status=status.HTTP_200_OK)
        elif user.user_type == "content_creator":
            all_postings = ContentCreatorPostingSerializer(Posting.objects.all(), many=True, context={'user': user})
            return Response(all_postings.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        posting = get_object_or_404(Posting, pk=kwargs["pk"])
        serializer = PostingSubmissionsSerializer(posting)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # @action(detail=False, methods=['post'])
    # def get_ads(self, request, pk=None):
