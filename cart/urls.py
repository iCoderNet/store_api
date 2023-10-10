from django.urls import re_path, path
from . import views

urlpatterns = [
    path('cart/', views.view_cart),
    path('cart/<int:item_id>/', views.cart_item),
]