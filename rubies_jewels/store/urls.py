from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('shop/', views.shop, name='shop'),
    path('shop/<int:category_id>/', views.shop_category, name='shop_category'),
    path('upload/', views.upload, name='upload'),
    path('product/<int:product_id>/', views.product, name='product'),
]