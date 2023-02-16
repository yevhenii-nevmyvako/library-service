from django.urls import path, include
from rest_framework import routers
from .views import PaymentViewSet

router = routers.DefaultRouter()
router.register("payments", PaymentViewSet, basename="payment")

urlpatterns = [path("", include(router.urls))]

app_name = "payments"
