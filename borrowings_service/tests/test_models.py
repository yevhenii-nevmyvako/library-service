from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from book_service.models import Book
from borrowings_service.models import Borrowings


class BorrowingModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            email="test@tesing.com",
            password="wsx2wsx2",
            first_name="Marlen",
            last_name="Twong",
        )
        self.book = Book.objects.create(
            title="Harry Potter",
            author="Joahn rowling",
            cover="Hard",
            inventory=13.99,
            daily_fee=8.00,
        )
        self.borrowing = Borrowings.objects.create(
            borrow_date="2023-01-03",
            expected_return_date="2023-01-08",
            actual_return_date="2023-01-08",
            book=self.book,
            user=self.user,
        )

    def test_borrowing_str(self):
        """test representation method in models"""
        self.assertEqual(
            str(self.borrowing),
            f"{self.borrowing.user} borrowed {self.borrowing.book} "
            f"{self.borrowing.borrow_date}",
        )

    def test_borrow_date_greater_then_expected_return_date(self):
        """test validation for expected return date"""
        self.borrowing.borrow_date = "2023-01-10"
        with self.assertRaises(ValidationError):
            self.borrowing.full_clean()

    def test_borrow_date_greater_then_actual_return_date(self):
        """test validation for actual return date"""
        self.borrowing.borrow_date = "2023-01-10"
        with self.assertRaises(ValidationError):
            self.borrowing.full_clean()
