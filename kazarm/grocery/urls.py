from django.urls import path, include
from . import views

app_name = 'grocery'

urlpatterns = [
    path('', views.productList, name='product-list'),
    path('add-product', views.product_create, name='product_create'),
    path('edit/<int:f_s_id>/', views.product_edit, name='product_edit'),
]
