from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubmissionViewSet

# Create a router and register the viewset
router = DefaultRouter()
router.register(r'submissions', SubmissionViewSet)

# Wire up the router URLs
urlpatterns = [
    path('api/', include(router.urls)),
]