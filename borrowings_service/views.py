from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from borrowings_service.models import Borrowings
from borrowings_service.serializers import BorrowingsSerializer


class BorrowingsViewSet(viewsets.ModelViewSet):
    queryset = Borrowings.objects.all()
    serializer_class = BorrowingsSerializer
    permission_classes = (AllowAny,)
