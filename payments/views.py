
from rest_framework import viewsets


from pagination import LibraryPagination
from payments.models import Payment


from payments.serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    pagination_class = LibraryPagination
    # permission_classes = [IsAuthenticated]

















