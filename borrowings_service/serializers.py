from django.db import transaction
from rest_framework import serializers

from book_service.serializers import BookSerializer
from borrowings_service.models import Borrowings


class BorrowingsSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        with transaction.atomic():
            book = validated_data.get("book_id")
            borrowing = Borrowings.objects.create(**validated_data)
            book.inventory -= 1
            book.save()

            return borrowing


class BorrowingsListSerializer(serializers.ModelSerializer):
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


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowings
        fields = ("actual_return_date",)
