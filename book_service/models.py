from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "Hard"
        SOFT = "Soft"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=5, choices=CoverChoices.choices)
    inventory = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0,
    )
    daily_free = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(99999)],
        default=0,
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "Books"
        verbose_name_plural = "Books"

    def __str__(self) -> str:
        return self.title
