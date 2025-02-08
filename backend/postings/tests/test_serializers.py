from django.test import TestCase  # Change SimpleTestCase to TestCase
from postings.serializers import PostingSerializer
from users.models import User  # Import User model
from postings.models import Posting
from decimal import Decimal

class PostingSerializerTest(TestCase):  # Use TestCase instead of SimpleTestCase

    def setUp(self):
        """Create a test user and mock data for serializer tests"""
        self.user = User.objects.create(username="testuser")  # Create a real user

        self.valid_data = {
            "creator": self.user.id,  # Use actual user ID
            "title": "Marketing Campaign",
            "description": "This is a test campaign for a new product.",
            "price_per_click": Decimal("0.0500"),
            "deadline": "2024-12-31T23:59:59Z",
            "percentage_cut": Decimal("0.30"),
            "is_active": True,
            "keywords": ["marketing", "ads"]
        }

        self.invalid_data = {
            "creator": self.user.id,  # Use actual user ID
            "title": "",  # Missing title (should fail)
            "description": "Test campaign description",
            "price_per_click": Decimal("-0.01"),  # Negative price (should fail)
            "deadline": "2024-12-31T23:59:59Z",
            "percentage_cut": Decimal("1.50"),  # Exceeds 1.00 limit (should fail)
            "is_active": True,
            "keywords": "marketing, ads"  # Should be a list, not a string
        }

    def test_valid_posting_serializer(self):
        """Test serializer with valid data"""
        serializer = PostingSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)  # Show errors if it fails
        self.assertEqual(serializer.validated_data["title"], "Marketing Campaign")

    def test_invalid_posting_serializer(self):
        """Test serializer with invalid data"""
        serializer = PostingSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())  # Expecting failure
        self.assertIn("title", serializer.errors)  # Title is required
        self.assertIn("price_per_click", serializer.errors)  # Negative value should fail
        self.assertIn("percentage_cut", serializer.errors)  # Out-of-range value should fail
        self.assertIn("keywords", serializer.errors)  # Should be a list, not a string
