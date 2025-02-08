from .views import PostingViewSet


# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'postings', PostingViewSet)  # This automatically creates API endpoints

urlpatterns = [
    path('', include(router.urls)),  # Includes the auto-generated routes
]
