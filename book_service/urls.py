from book_service.views import BookViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register("books", BookViewSet, basename="books")

urlpatterns = router.urls

app_name = "book_service"
