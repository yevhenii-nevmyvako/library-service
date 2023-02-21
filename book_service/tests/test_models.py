from django.test import TestCase

from book_service.models import Book


class BookModelTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Harry Potter",
            author="Joahn Rowling",
            cover="Hard",
            inventory=7,
            daily_fee=12.00,
        )

    def test_user_str(self):
        """test should check representation method in models, book_service"""
        self.assertEqual(str(self.book), f"{self.book.title}")
