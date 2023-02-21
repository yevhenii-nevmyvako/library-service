from rest_framework import viewsets, permissions

from book_service.models import Book
from book_service.serializers import BookSerializer
from pagination import LibraryPagination


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = LibraryPagination
    permission_classes = (permissions.IsAdminUser,)

    def get_permissions(self) -> permission_classes:
        if self.request.method in ["PUT", "DELETE", "PATCH", "POST"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
