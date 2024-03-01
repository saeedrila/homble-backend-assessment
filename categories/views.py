from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK
)

from .models import Category
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
    return Response({"categories": serializer.data}, status=HTTP_200_OK)