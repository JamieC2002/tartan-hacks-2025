from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError

from postings.models import Posting
from users.models import User

# Create your models here.
class Submission(models.Model):
    poster = models.ForeignKey(Posting, on_delete=models.CASCADE, related_name = 'submissions')
    time_submit = models.DateTimeField(auto_now_add = True)
    submitter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_creator')
    image = models.URLField(blank=True, null=True)  # Optional field
    video = models.URLField(blank=True, null=True)  # Optional field
    qualify = models.BooleanField(default=False)
    keywords = models.JSONField(blank = True, default = list)
    description = models.TextField(default="")

    def clean(self):
        super().clean()  # Call the parent's clean method to ensure other validations are run

        # Custom validation: Either image OR video must be provided
        if not self.image and not self.video:
            raise ValidationError("Either an image or a video must be provided.")

    def __str__(self):
        return f"Submission by {self.submitter} at {self.time_submit}"