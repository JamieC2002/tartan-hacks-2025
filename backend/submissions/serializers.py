from rest_framework import serializers
from .models import Submission

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'poster', 'time_submitted', 'submitter', 'image', 'video', 'qualify', 'keywords', 'description']
    
    # Custom validation to ensure either image or video is provided
    def validate(self, data):
        if not data.get('image') and not data.get('video'):
            raise serializers.ValidationError("Either an image or a video must be provided.")
        return data
