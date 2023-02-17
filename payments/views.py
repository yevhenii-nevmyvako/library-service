from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from pagination import LibraryPagination
from payments.models import Payment

from payments.serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    pagination_class = LibraryPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_staff is False:
            return Payment.objects.filter(borrowing__user=current_user)
        return Payment.objects.all()

    @action(
        methods=["GET"],
        detail=True,
        url_path="success",
        permission_classes=[IsAuthenticated],
    )
    def success_url(self, request, pk=None) -> Response:
        session_id = request.GET.get("session_id")
        payment = Payment.objects.get(session_id=session_id)
        payment.save()
        return Response(status=status.HTTP_200_OK)

    @action(methods=["GET"],
            detail=True,
            url_path="cancel",
            permission_classes=[IsAuthenticated],
            )
    def cancel_url(self, request, pk=None) -> Response:
        return Response(status=status.HTTP_400_BAD_REQUEST)
