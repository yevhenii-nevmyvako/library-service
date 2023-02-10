from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import QuerySet
from drf_spectacular.types import OpenApiTypes
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import OpenApiParameter, extend_schema
from borrowings_service.models import Borrowings
from borrowings_service.serializers import (
    BorrowingsSerializer,
    BorrowingsDetailSerializer,
    BorrowingsListSerializer,
    BorrowingReturnBookSerializer,
    BorrowingsCreateSerializer,
)
from pagination import LibraryPagination


class BorrowingsViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowings.objects.all().select_related("book")
    serializer_class = BorrowingsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LibraryPagination

    @staticmethod
    def get_parameter(parameter: str) -> bool:
        if parameter == "active":
            return True
        elif parameter == "returned":
            return False

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset
        is_active = self.get_parameter(
            self.request.query_params.get("is_active")
        )
        user_id = self.request.query_params.get("user_id")

        if is_active is not None:
            queryset = queryset.filter(actual_return_date__isnull=is_active)

        if self.request.user.is_staff:
            if user_id is not None:
                queryset = queryset.filter(user_id=user_id)

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user.id)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingsListSerializer

        if self.action == "retrieve":
            return BorrowingsDetailSerializer

        if self.action == "create":
            return BorrowingsCreateSerializer

        if self.action == "return_book":
            return BorrowingReturnBookSerializer

        return BorrowingsSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        methods=["POST"],
        detail=True,
        url_path="return_book",
        permission_classes=[IsAuthenticated],
    )
    def return_book(self, request, pk=None):
        """Endpoint for returning borrowing book"""
        borrowing = self.get_object()
        book = borrowing.book
        serializer = self.get_serializer(borrowing, data=request.data)

        if borrowing.actual_return_date is not None:
            raise ValidationError("Book have already returned")

        if serializer.is_valid():
            Borrowings.validate_date(
                borrowing.borrow_date,
                borrowing.expected_return_date,
                serializer.validated_data["actual_return_date"],
                ValidationError,
            )
            with transaction.atomic():
                serializer.save()
                book.inventory += 1
                book.save()

                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="is_active",
                type=OpenApiTypes.STR,
                description="Filter by active borrowings (ex. ?is_active=True)",
            ),
            OpenApiParameter(
                "user_id",
                type=OpenApiTypes.INT,
                description="Filter by user id if user is_stuff (ex. ?user_id=(1, 2, 3))",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
