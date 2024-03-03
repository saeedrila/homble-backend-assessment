from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Count

from .models import Category
from products.models import Sku
from .serializers import CategorySerializer


@api_view(["GET"])
@permission_classes([IsAdminUser])
def categories_list(request):
    """
    Lists all categories and their corresponding products.
    permission restricted to admin, staff.
    For testing purpose, permission has been given to any users.
    """
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response({"categories": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def queryset_active_categories(request):
    """
    Queryset to fetch categories that are active, along with their respective SKU count.
    """
    my_queryset = (
        Category.objects.filter(
            products__sku__status=Sku.Status.APPROVED, is_active=True
        )
        .prefetch_related("products__sku")
        .annotate(approved_sku_count=Count("products__sku", distinct=True))
    )

    for category in my_queryset:
        print(
            f"Category: {category.name}; Approved SKU Count: {category.approved_sku_count}"
        )

    return Response(status=status.HTTP_200_OK)
