from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Posting
from .serializers import PostingSerializer


class PostingViewSet(viewsets.ModelViewSet):
    """Handles CRUD operations for postings"""
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer
