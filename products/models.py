from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    """
    Products model consists of product name, description, category, etc.
    """

    name = models.CharField(
        _("display name"),
        max_length=150,
        unique=True,
        help_text=_("This will be displayed to user as-is"),
    )
    description = models.TextField(
        _("descriptive write-up"),
        unique=True,
        help_text=_("Few sentences that showcase the appeal of the product"),
    )
    ingredients = models.CharField(
        _("ingredients"),
        max_length=500,
        blank=True,
        null=True,
        help_text=_("contents of the product"),
    )
    is_refrigerated = models.BooleanField(
        help_text=_("Whether the product needs to be refrigerated"),
        default=False,
    )
    category = models.ForeignKey(
        "categories.Category",
        related_name="products",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    managed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="managed_products",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.name = self.name.strip().title()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        # Just to be explicit.
        db_table = "product"
        ordering = []
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Sku(models.Model):
    """
    SKU (Stock Keeping Unit) consists of product model, size, and price details.
    Admin adds platform commission and cost_price details.
    Selling price will be calculated and automatically saved.
    """

    product = models.ForeignKey(
        Product,
        related_name="sku",
        on_delete=models.CASCADE,
    )
    size = models.PositiveSmallIntegerField(
        _("Size (in grams)"),
        help_text=_("Size of SKU in grams"),
    )
    selling_price = models.PositiveSmallIntegerField(
        _("Selling price (Rs.)"),
        help_text=_("Price payable by customer (Rs.)"),
    )
    platform_commission = models.PositiveSmallIntegerField(
        _("Platform commission (Rs.)"),
        help_text=_("Commission for platform (Rs.)"),
    )
    cost_price = models.PositiveSmallIntegerField(
        _("Cost price (Rs.)"),
        help_text=_("Cost price (Rs.)"),
    )

    def save(self, *args, **kwargs):
        self.selling_price = self.cost_price + self.platform_commission
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name}: {self.size}gm (Rs.{self.selling_price})"
