from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('shop/', views.shop, name='shop'),
    path('handle_email/', views.handle_email, name='handle_email'),
    path('product/<int:product_id>/', views.product, name='product'),
]