from rest_framework import serializers
from .models import Posting

class PostingSerializer(serializers.ModelSerializer):
    creator_username = serializers.CharField(source='creator.username', read_only=True)
    
    def validate_keywords(self, value):
        """Ensure that keywords is always a list of strings"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Keywords must be a list.")
        if any(not isinstance(word, str) for word in value):
            raise serializers.ValidationError("Each keyword must be a string.")
        return value
    
    class Meta:
        model = Posting
        fields = '__all__'

        
        
