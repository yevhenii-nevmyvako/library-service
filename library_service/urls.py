"""library_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework import routers

from book_service.urls import router as books
from borrowings_service.urls import router as borrowings
# from payment.urls import router as payments
router = routers.DefaultRouter()
router.registry.extend(books.registry)
router.registry.extend(borrowings.registry)
# router.registry.extend(payments.registry)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/", include(router.urls)),
    path("api/users/", include("user.urls", namespace="users")),
    path("api/doc/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/doc/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/doc/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
