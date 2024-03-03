from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Sku
from .serializers import (
    ProductListSerializer,
    SkuSerializer,
    ProductDetailSerializer,
    ProductDetailsWithSkuSerializer,
)


@api_view(["GET"])
@permission_classes([AllowAny])
def products_list(request):
    """
    List of all products. The request can have a query paramerter 'refregerated = True'
    or false. This will return the product list that adhere to the criteria.
    """

    refregerated_param = request.query_params.get("refregerated", None)

    if refregerated_param is not None:
        refegerated = refregerated_param.lower() == "true"
        products = Product.objects.filter(is_refrigerated=refegerated)
    else:
        products = Product.objects.all()
    serializer = ProductListSerializer(products, many=True)
    return Response({"products": serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_sku(request):
    """
    Helps create new SKUs. Permission: only for Admin/Staff users.
    """
    serializer = SkuSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(status=Sku.Status.PENDING)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAdminUser])
def update_sku_status(request):
    """
    Updates SKU status. Permission: only for Admin/Staff users.
    """
    sku_id = request.GET.get("sku_id")
    new_status = request.GET.get("status").upper()
    status_options = {"PENDING": 0, "APPROVED": 1, "DISCONTINUED": 2}
    try:
        sku = Sku.objects.get(id=sku_id)
        if new_status in status_options:
            sku.status = status_options[new_status]
            sku.save()
            return Response(
                {"Details": "SKU udpated successfully"}, status=status.HTTP_202_ACCEPTED
            )
        else:
            return Response(
                {"Details": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST
            )

    except Sku.DoesNotExist:
        return Response(
            {"Details": "Sku is not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_sku(request):
    """
    Deletes SKU. To delete newly created SKU with Postman API testing.
    Permission: only for Admin/Staff users.
    """
    try:
        sku_id = request.GET.get("sku_id")
        sku = Sku.objects.get(id=sku_id)
    except Sku.DoesNotExist:
        return Response({"Details": "SKU not found"}, status=status.HTTP_404_NOT_FOUND)

    sku.delete()
    return Response(
        {"Details": "SKU has been deleted successfully"},
        status=status.HTTP_204_NO_CONTENT,
    )


# Check.
@api_view(["GET"])
def product_detail(request, product_id):
    """
    Returns product details corresponding to product_id.
    """
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response(
            {"Details": "Product not found"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = ProductDetailSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def product_detail_with_sku(request):
    """
    Product along with it's related SKUs.
    """
    try:
        product_id = request.GET.get("product_id")
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {"Details": "Product not found"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = ProductDetailsWithSkuSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)
