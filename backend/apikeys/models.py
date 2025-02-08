from django.db import models
from users.models import User

# Create your models here.
class APIKey(models.Model):
    owner = models.ForeignKey(User, related_name="api_keys", on_delete=models.CASCADE)
    value = models.CharField(max_length=1024)
