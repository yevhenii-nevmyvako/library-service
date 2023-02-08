from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from borrowings_service.models import Borrowings
from borrowings_service.serializers import (
    BorrowingsSerializer,
    BorrowingsDetailSerializer,
    BorrowingsListSerializer,
    # BorrowingsListSerializer,
)


class BorrowingsViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowings.objects.all().select_related("book")
    serializer_class = BorrowingsSerializer
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingsListSerializer

        if self.action == "retrieve":
            return BorrowingsDetailSerializer

        return BorrowingsSerializer

    # def get_queryset(self):
    #     queryset = self.queryset
    #     is_active = self._get_bool_from_param(
    #         self.request.query_params.get("is_active")
    #     )
    #     user_id = self.request.query_params.get("user_id")
    #
    #     if is_active is not None:
    #         queryset = queryset.filter(actual_return_date__isnull=is_active)
    #
    #     if self.request.user.is_staff and user_id is not None:
    #         queryset = queryset.filter(user_id=user_id)
    #
    #     if not self.request.user.is_staff:
    #         queryset = queryset.filter(user=self.request.user.id)
    #
    #     return queryset
