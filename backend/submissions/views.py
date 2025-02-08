from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from submissions.models import Submission
from submissions.serializers import SubmissionSerializer
from submissions.utilities import calculate_similarity
from rest_framework import status

class SubmissionViewSet(GenericViewSet):
    # QuerySet defines which data to fetch (all submissions in this case)
    queryset = Submission.objects.all()

    # Serializer specifies how to convert the model data to JSON
    serializer_class = SubmissionSerializer

    @action(detail=False, methods=["POST"], url_path="create")
    def create_submission(self, request, *args, **kwargs):
        serializer = SubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"], url_path="filter-by-keywords")
    def filter_by_keywords(self, request):
        """
        Custom GET action to filter submissions by matching keywords and checking 'qualify' status.
        """
        # Retrieve keywords from posting
        search_term = request.query_params.get('keyword', None)  # Get the search keyword from the query params
        if not search_term:
            return Response({"error": "keyword parameter is required"}, status=400)

        # Filter by submissions that have 'qualify=True'
        queryset = Submission.objects.filter(qualify=True)

        # Further filter submissions based on matching keywords
        filtered_submissions = [
            submission for submission in queryset
            if calculate_similarity(submission, search_term)
        ]
        
        # Process filtered_submissions to retireve top N submissions

        # Serialize the filtered submissions
        serializer = self.get_serializer(filtered_submissions, many=True)
        
        # Return the filtered list of submissions
        return Response(serializer.data)
