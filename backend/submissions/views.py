from django.http import HttpResponse
from django.templatetags.static import static
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Submission
from .serializers import SubmissionSerializer
from tartan_ads.utilities import calculate_similarity
from submissions.models import Submission
from submissions.serializers import SubmissionSerializer
from rest_framework import status
from tartan_ads.file2keyword import extract_keywords_from_video, extract_keywords_from_picture

import threading


class SubmissionViewSet(GenericViewSet):
    # QuerySet defines which data to fetch (all submissions in this case)
    queryset = Submission.objects.all()

    # Serializer specifies how to convert the model data to JSON
    serializer_class = SubmissionSerializer
    
    @action(detail=False, methods=["GET"], url_path="test")
    def test(self, request):
        """Return an HTML page displaying the MP4 video with autoplay and unmute button"""
        
        video_url = "https://www.w3schools.com/tags/movie.mp4"  # Sample video URL

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Test Video</title>
        </head>
        <body>

            <h2>MP4 Video Test</h2>

            <video id="myVideo" width="560" height="315" autoplay muted playsinline controls>
                <source src="{video_url}" type="video/mp4">
                Your browser does not support the video tag.
            </video>

        </body>
        </html>
        """
        return HttpResponse(html_content, content_type="text/html")  

    """
    APIs
    
    Get Posting keywords -> Posting viewset
    """
    @action(detail=False, methods=["POST"], url_path="create")
    def create_submission(self, request, *args, **kwargs):
        def process_save_submission(request_data):
            if request_data.get("video"):
                video_url = request_data.get("video")
                keywords = extract_keywords_from_video(video_url)
                request_data["keywords"] = keywords
            elif request_data.get("image"):
                image_url = request_data.get("image")
                print("image_url here:", image_url)
                keywords = extract_keywords_from_picture(image_url)
                request_data["keywords"] = keywords
            serializer = SubmissionSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
            print("create_submission errs:", serializer.errors)
        t = threading.Thread(target=process_save_submission, args=(request.data,))
        t.start()
        return Response(status=status.HTTP_200_OK)

    
    @action(detail=True, methods=["GET"], url_path="toggle-accept")
    def toggle_accept(self, request, *args, **kwargs):
        submission = self.get_object()
        submission.qualify = not submission.qualify
        return Response(status=status.HTTP_200_OK)

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
        
        # Process filtered_submissions to retrieve top N submissions
        # Map to the Submission Objects

        # Serialize the filtered submissions
        serializer = self.get_serializer(filtered_submissions, many=True)
        
        # Return the filtered list of submissions
        return Response(serializer.data)
