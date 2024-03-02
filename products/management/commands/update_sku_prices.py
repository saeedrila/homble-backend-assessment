from django.core.management.base import BaseCommand
from products.models import Sku
from django.db import models


class Command(BaseCommand):
    """
    This is helpful when platform and cost_price needed to be auto populated.
    """

    help = "This updates the selling price of existing Sku records."

    def handle(self, *args, **kwargs):
        Sku.objects.update(
            platform_commission=models.F("selling_price") * 0.25,
            cost_price=models.F("selling_price") - models.F("platform_commission"),
        )

        self.stdout.write(
            self.style.SUCCESS("Successfully updated selling_price for existing Skus")
        )
