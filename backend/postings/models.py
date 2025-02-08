from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator

from users.models import User

class Posting(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="postings")
    title = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(3)] 
    )
    description = models.TextField()
    deadline = models.DateTimeField()
    # format: $0.0000 <= $xx.xxxx <= $99.9999
    price_per_click = models.DecimalField(
        max_digits=6, 
        decimal_places=4, 
        default=Decimal("0.0000"),
        validators=[MinValueValidator(Decimal("0.0000"))]
    )
    # format: 0.00 <= x.xxx <= 1.00
    percentage_cut = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.00,
        validators=[MinValueValidator(Decimal("0.00")), MaxValueValidator(Decimal("1.00"))]
    )
    is_active = models.BooleanField(default=True)
    # JSON List: must contain strings
    keywords = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return f"{self.title} by {self.creator.username}"