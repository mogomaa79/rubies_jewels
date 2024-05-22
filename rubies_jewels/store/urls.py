from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('shop/', views.shop, name='shop'),
    path('blog/', views.blog, name='blog'),
    path('handle_email/', views.handle_email, name='handle_email'),
]