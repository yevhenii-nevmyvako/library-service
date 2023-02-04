from django.db import models
from django.utils import timezone

from book_service.models import Book
from user.models import User


def default_time_to_expected_return_date():
    return timezone.now() + timezone.timedelta(days=1)


class Borrowings(models.Model):
    borrow_date = models.DateTimeField(auto_now_add=False)
    expected_return_date = models.DateTimeField(
        auto_now_add=False, default=default_time_to_expected_return_date()
    )
    actual_return_date = models.DateTimeField(auto_now_add=False)
    book_id = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="borrowings"
    )
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="borrowings"
    )

    class Meta:
        ordering = ["expected_return_date"]
        verbose_name_plural = "Borrowings"
        verbose_name = "Borrowings"

    def __str__(self):
        return self.expected_return_date
