from django.contrib import admin

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "cover",
        "inventory",
        "daily_fee_with_usd",
    ]
    list_filter = ("title", "author")
