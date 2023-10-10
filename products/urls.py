from django.urls import re_path, path
from . import views

urlpatterns = [
    path('category/', views.category_list),
    path('category/<int:cid>/', views.category_detail),
    path('product/', views.product_list),
    path('product/<int:pk>', views.product_detail),
    path('review/', views.review_list),
    path('review/<int:pk>', views.review_detail),
]