from django.urls import path
from .views import (
    search_product
)

urlpatterns = [
    path("search-product-pos/", search_product, name="search_product_pos"),
]