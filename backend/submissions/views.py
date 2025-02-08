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
        submission.save()
        return Response(status=status.HTTP_200_OK)