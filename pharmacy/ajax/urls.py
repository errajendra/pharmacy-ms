from django.urls import path
from .views import (
    search_product, load_cart_items, add_to_cart, cart_item_update,
)

urlpatterns = [
    path("search-product-pos/", search_product, name="search_product_pos"),
    path("load-cart-items-pos/", load_cart_items, name="load_cart_items_pos"),
    path("add-to-cart-pos/", add_to_cart, name="add_to_cart_pos"),
    path("update-cart-pos/", cart_item_update, name="cart_item_update_pos"),
]