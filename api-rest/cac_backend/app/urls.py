from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('products', views.get_products, name='get_products'),
  path('products/<int:pk>', views.get_product, name='get_product'),
  path('users', views.get_users, name='get_users'),
  path('users/<int:pk>', views.get_user, name='get_user'),
  path('auth/login', views.login, name='login'),
  path('auth/register', views.register, name='register'),  
]