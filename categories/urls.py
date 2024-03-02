from django.urls import path

from .views import categories_list

urlpatterns = [path("", categories_list, name="categories-list")]
