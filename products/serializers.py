from rest_framework import serializers

from products.models import Product


class ProductListSerializer(serializers.ModelSerializer):
    """
    Serializer to show list of products.
    """

    class Meta:
        model = Product
        fields = ["name"]
