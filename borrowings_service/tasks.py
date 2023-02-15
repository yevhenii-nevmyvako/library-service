from datetime import date, timedelta
import datetime
from celery import shared_task

from book_service.models import Book
from borrowings_service.models import Borrowings
from user.models import User
from borrowings_service.borrowing_notifications_bot import send_message


@shared_task
def overdue_notifications() -> send_message:
    last_day = date.today() + timedelta(days=1)
    overdue = Borrowings.objects.filter(
        expected_return_date__lte=last_day
    ).values(
        "book", "user", "expected_return_date",
    )
    if overdue:
        for borrowing in overdue:
            days_late = last_day - borrowing["expected_return_date"]
            book = Book.objects.get(id=borrowing["book"])
            user = User.objects.get(id=borrowing["user"])
            message = f"{user.first_name} {user.last_name} \n" \
                      f"Have {days_late} to return the {book.title} \n" \
                      f"before it overdue"
            send_message(message)

