from django.shortcuts import render
from submissions.models import Submission
from tartan_ads.utilities import calculate_similarity
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from postings.models import Posting
from postings.serializers import PostingSerializer, ShowPostingSerializer, PostingSubmissionsSerializer, ContentCreatorPostingSerializer
from users.models import User
from django.shortcuts import get_object_or_404

class PostingViewSet(viewsets.ModelViewSet):
    """Handles CRUD operations for postings"""
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get("user_id", None)
        
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if user.user_type == "brand":
            user_postings = ShowPostingSerializer(user.postings.all(), many=True)
            return Response(user_postings.data, status=status.HTTP_200_OK)
        elif user.user_type == "content_creator":
            all_postings = ContentCreatorPostingSerializer(Posting.objects.all(), many=True, context={'user': user})
            return Response(all_postings.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        posting = get_object_or_404(Posting, pk=kwargs["pk"])
        serializer = PostingSubmissionsSerializer(posting)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'], url_path="get-ads")
    def get_ads(self, request):
        search_term = request.query_params.get('queryset', None)  # Get query string parameter
        if not search_term:
            return Response({"detail": "queryset parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        search_keywords = search_term.split(",")  # Convert query string to a list
        def best_posting():

            best_dist = -1
            best_post = None

            for postings in self.queryset:
                temp = calculate_similarity(postings.keywords, search_term)
                if temp > best_dist:
                    best_dist = temp
                    best_post = postings
            
            if best_dist == -1 or best_post == None:
                return None #raise an error
                
            return best_post
        
        sel_post = best_posting()

        if sel_post is None:
            return Response({"detail": "No matching posting found."}, status=status.HTTP_404_NOT_FOUND)

        def best_sub4post(posting):
            best_dist = -1
            best_sub = None

            filtered_submissions = [
                submission for submission in Submission.objects.all()
                if submission.qualify and submission.poster == posting
            ]

            for submission in filtered_submissions:
                temp = calculate_similarity(submission.keywords, posting.keywords)
                if temp > best_dist:
                    best_dist = temp
                    best_sub = submission
            if best_dist == -1 or best_sub == None:
                return None #raise an error
                
            return best_sub
        
        sel_sub = best_sub4post(sel_post)

        if sel_sub is None:
            return Response({"detail": "No matching submission found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(sel_sub)

        return Response(serializer.data)

    # @action(detail=False, methods=['post'])
    # def get_ads(self, request, pk=None):
