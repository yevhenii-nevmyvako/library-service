from django.urls import path, include

from book_service.views import BookViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register("books", BookViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "book_service"
