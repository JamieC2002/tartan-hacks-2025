from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and returns a regular user with email as username."""
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        extra_fields.setdefault("username", email)  # Set username as email

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and returns a superuser, ensuring username is email."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)  

class User(AbstractUser):
    email = models.CharField(max_length=1024, unique=True)
    username = models.CharField(max_length=1024, blank=True, null=True, unique=False)
    password = models.CharField(max_length=1024)
    USER_TYPE_CHOICES = [
        ("brand", "Brand"),
        ("content_creator", "Content Creator"),
        ("developer", "Developer"),
    ]
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=20)
    # only for content creators, developers
    money_earned = models.FloatField(default=0)
    # only for developers
    developer_api_key = models.CharField(max_length=50, blank=True, null=True)
    # only for brands
    brand_budget = models.FloatField(default=0)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

