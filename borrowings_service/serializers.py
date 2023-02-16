from django.db import transaction
from rest_framework import serializers

from book_service.serializers import BookSerializer
from borrowings_service.borrowing_notifications_bot import send_message
from borrowings_service.models import Borrowings


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
    user_full_name = serializers.StringRelatedField(read_only=True)
    book_info = BookSerializer(many=False, read_only=True)

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

    def create(self, validated_data) -> object:
        with transaction.atomic():
            book = validated_data.get("book")
            borrowing = Borrowings.objects.create(**validated_data)
            book.inventory -= 1
            book.save()
            message = f"Create new borrowing " \
                      f"at: {borrowing.borrow_date}\n" \
                      f"Book Title: {borrowing.book.title}\n" \
                      f"User: {borrowing.user}\n" \
                      f"Expected return date: " \
                      f"{borrowing.expected_return_date}\n"
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

    def validate_book(self, value) -> int:
        if value.inventory == 0:
            message = f"Sorry no books left with this title"
            send_message(message)
            raise serializers.ValidationError("Books with this title are over")
        return value


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
    book_info = BookSerializer(many=False, read_only=True)
    user_full_name = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Borrowings
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_info",
            "user_full_name",
        )


class BorrowingReturnBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowings
        fields = ("actual_return_date",)
