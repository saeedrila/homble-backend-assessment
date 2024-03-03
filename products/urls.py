from django.urls import path

from .views import (
    products_list,
    create_sku,
    delete_sku,
    product_detail_with_sku,
    update_sku_status,
)


urlpatterns = [
    path("", products_list, name="products-list"),
    path("details-with-sku/", product_detail_with_sku, name="product-details-with-sku"),
    path("create-sku/", create_sku, name="create-sku"),
    path("update-sku-status/", update_sku_status, name="update-sku-status"),
    path("delete-sku/", delete_sku, name="delete-sku"),
]
