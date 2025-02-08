from rest_framework import serializers
from submissions.models import Submission

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'poster', 'time_submit', 'submitter', 'image', 'video', 'qualify', 'keywords', 'description']
    
    # Custom validation to ensure either image or video is provided
    def validate(self, data):
        if not data.get('image') and not data.get('video'):
            raise serializers.ValidationError("Either an image or a video must be provided.")
        return data
    
    


class ShowSubmissionSerializer(serializers.ModelSerializer):
    submitter = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = ['id', 'poster', 'time_submit', 'submitter', 'image', 'video', 'qualify', 'keywords', 'description']

    def get_submitter(self, obj):
        return obj.submitter.email
