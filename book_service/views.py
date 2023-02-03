from rest_framework import viewsets, permissions

from book_service.models import Book
from book_service.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE", "PATCH", "POST"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
