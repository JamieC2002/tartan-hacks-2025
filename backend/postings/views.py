from django.shortcuts import render
from django.urls import path, include
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.routers import DefaultRouter
from .models import Posting
from .serializers import PostingSerializer
from .views import PostingViewSet

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'postings', PostingViewSet)  # This automatically creates API endpoints

urlpatterns = [
    path('', include(router.urls)),  # Includes the auto-generated routes
]

class PostingViewSet(viewsets.ModelViewSet):
    """Handles CRUD operations for postings"""
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]