from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Submission
from .serializers import SubmissionSerializer

class SubmissionViewSet(GenericViewSet):
    # QuerySet defines which data to fetch (all submissions in this case)
    queryset = Submission.objects.all()

    # Serializer specifies how to convert the model data to JSON
    serializer_class = SubmissionSerializer
