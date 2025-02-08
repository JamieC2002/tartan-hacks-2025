from rest_framework import serializers
from postings.models import Posting
from users.models import User
from submissions.serializers import ShowSubmissionSerializer

class PostingSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )

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

class ShowPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posting
        fields = '__all__'

class ContentCreatorPostingSerializer(serializers.ModelSerializer):
    has_submitted = serializers.SerializerMethodField()

    class Meta:
        model = Posting
        fields = '__all__'

    def get_has_submitted(self, obj):
        curr_user = self.context.get('user')
        user_submissions = obj.submissions.filter(submitter=curr_user)
        return len(user_submissions) > 0

class PostingSubmissionsSerializer(serializers.ModelSerializer):
    submissions = serializers.SerializerMethodField()

    class Meta:
        model = Posting
        fields = '__all__'

    def get_submissions(self, obj):
        submissions = obj.submissions.all()
        print("submissions:", submissions)
        return ShowSubmissionSerializer(submissions, many=True).data
