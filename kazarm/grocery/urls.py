from django.urls import path, include
from . import views

app_name = 'grocery'

urlpatterns = [
    path('', views.first_stage_list, name='product-list'),
    path('add-product/', views.first_stage_create, name='product_create'),
    path('edit/<int:f_s_id>/', views.first_stage_edit, name='product_edit'),
    path('add-type-product/', views.product_create, name='product_type_add'),
    path('containers/', views.container_list, name='containers_list'),
    path('containers/create/', views.container_create, name='container_create'),
    path('containers/edit/<int:container_id>', views.container_edit, name='container_edit')
]
