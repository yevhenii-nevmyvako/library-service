from django.db import transaction
from rest_framework import serializers

from book_service.models import Book
from borrowings_service.borrowing_notifications_bot import send_message
from borrowings_service.models import Borrowings
from payments.serializers import PaymentSerializer


class BorrowingsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Borrowings
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )


class BorrowingsCreateSerializer(serializers.ModelSerializer):
    book_info = serializers.CharField(source="book", read_only=True)
    user_full_name = serializers.CharField(source="user", read_only=True)

    class Meta:
        model = Borrowings
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user_full_name",
            "book_info",
        )

    def create(self, validated_data) -> Borrowings:
        with transaction.atomic():
            book = validated_data.get("book")
            borrowing = Borrowings.objects.create(**validated_data)
            book.inventory -= 1
            book.save()
            message = (f"Create new borrowing at: {borrowing.borrow_date}\n"
                       f"Book Title: {borrowing.book.title}\n"
                       f"User: {borrowing.user}\n"
                       f"Expected return date: "
                       f"{borrowing.expected_return_date}\n")
            send_message(message)
            return borrowing

    def validate(self, attrs) -> dict:
        data = super().validate(attrs=attrs)
        Borrowings.validate_date(
            attrs.get("borrow_date"),
            attrs.get("expected_return_date"),
            attrs.get("actual_return_date"),
            serializers.ValidationError,
        )

        return data

    def validate_book(self, book_value: Book) -> Book:
        if book_value.inventory == 0:
            message = f"Sorry no books left with this title"
            send_message(message)
            raise serializers.ValidationError("Books with this title are over")
        return book_value


class BorrowingsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowings
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
        )


class BorrowingsDetailSerializer(serializers.ModelSerializer):
    book_info = serializers.CharField(source="book", read_only=True)
    user_full_name = serializers.CharField(source="user", read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Borrowings
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_info",
            "user_full_name",
            "payments"
        )


class BorrowingReturnBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowings
        fields = ("actual_return_date",)
