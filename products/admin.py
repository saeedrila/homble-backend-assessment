from django.contrib import admin

from products.models import Product, Sku


class SkuInline(admin.TabularInline):
    """
    For displaying in ProductAdmin page.
    """

    model = Sku
    extra = 1
    ordering = ("-id",)
    readonly_fields = ("selling_price",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Product admin page configuration.
    """

    list_display = ("name", "managed_by")
    ordering = ("-id",)
    search_fields = ("name",)
    list_filter = ("is_refrigerated", "category")
    fields = (
        ("name"),
        ("category", "is_refrigerated"),
        "description",
        "ingredients",
        ("id", "created_at"),
        "managed_by",
    )
    autocomplete_fields = ("category", "managed_by")
    readonly_fields = ("id", "created_at")
    inlines = (SkuInline,)


class ProductInline(admin.StackedInline):
    """
    For displaying in CategoryAdmin.
    """

    model = Product
    extra = 0
    ordering = ("-id",)
    readonly_fields = ("name", "is_refrigerated")
    fields = (readonly_fields,)
    show_change_link = True


@admin.register(Sku)
class SkuAdmin(admin.ModelAdmin):
    """
    SKU admin page configuration.
    """

    list_display = (
        "product",
        "size",
        "cost_price",
        "platform_commission",
        "selling_price",
    )
    readonly_fields = ("selling_price",)
    search_fields = ("product__name", "size")
