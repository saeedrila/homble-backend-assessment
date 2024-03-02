from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """
    Category model. Count_product property added to count products that are
    related to a particular category.
    """

    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)

    @property
    def count_products(self):
        return self.products.count()

    def __str__(self):
        if self.is_active:
            return f"{self.name} (#{self.id})"
        else:
            return f"{self.name} [INACTIVE]"

    class Meta:
        db_table = "category"
        ordering = []
        verbose_name = "Category"
        verbose_name_plural = "Categories"
