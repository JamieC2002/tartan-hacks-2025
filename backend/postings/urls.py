from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostingViewSet

router = DefaultRouter()
router.register(r'postings', PostingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
