from rest_framework import serializers

from products.models import Product, Sku


class ProductListSerializer(serializers.ModelSerializer):
    """
    Serializer to show list of products.
    """

    class Meta:
        model = Product
        fields = ["name"]


class SkuSerializer(serializers.ModelSerializer):
    """
    Used for creating new SKUs.
    """

    selling_price = serializers.SerializerMethodField()

    def get_selling_price(self, sku):
        return sku.cost_price + sku.platform_commission

    def create(self, validated_data):
        return Sku.objects.create(**validated_data)

    class Meta:
        model = Sku
        fields = "__all__"


class ProductDetailsWithSkuSerializer(serializers.Serializer):
    """
    Used for serializing product along with its SKUs.
    """

    product = serializers.CharField(source="name", read_only=True)
    sku = SkuSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["product", "sku"]
