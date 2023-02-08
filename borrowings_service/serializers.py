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


class BorrowingsCreateSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        with transaction.atomic():
            book = validated_data.get("book")
            borrowing = Borrowings.objects.create(**validated_data)
            book.inventory -= 1
            book.save()

            return borrowing

    def validate(self, attrs):
        data = super().validate(attrs=attrs)
        Borrowings.validate_date(
            attrs.get("borrow_date"),
            attrs.get("expected_return_date"),
            attrs.get("actual_return_date"),
            serializers.ValidationError,
        )

        return data

    def validate_book(self, value):
        if value.inventory == 0:
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


class BorrowingReturnBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowings
        fields = ("actual_return_date",)
