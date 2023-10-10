from django.urls import re_path

from . import views

urlpatterns = [
    re_path('signup', views.signup),
    re_path('login', views.login),
    re_path('token/test', views.test_token),
    re_path('token/change', views.change_token),
]