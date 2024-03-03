from django.urls import path

from .views import (
    categories_list,
    queryset_active_categories,
)

urlpatterns = [
    path("", categories_list, name="categories-list"),
    # Querysets
    path(
        "queryset-active-categories/",
        queryset_active_categories,
        name="queryset-active-categories",
    ),
]
