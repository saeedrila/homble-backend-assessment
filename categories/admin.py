from django.contrib import admin

from categories.models import Category
from products.admin import ProductInline


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin page for category management.
    """

    list_display = ("id", "name", "is_active", "count_products")
    ordering = ("id",)
    search_fields = ("name",)
    list_filter = ("is_active",)
    fields = ("id", "name", "is_active", "count_products")
    readonly_fields = ("id", "count_products")
    inlines = (ProductInline,)
