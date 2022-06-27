from django.urls import path, include
from . import views

app_name = 'grocery'

urlpatterns = [
    path('', views.first_stage_list, name='product-list'),
    path('add-product/', views.first_stage_create, name='f_s_create'),
    path('edit/<int:f_s_id>/', views.first_stage_edit, name='f_s_edit'),
    path('add-type-product/', views.product_create, name='product_type_add'),
    path('containers/', views.container_list, name='containers_list'),
    path('containers/create/', views.container_create, name='container_create'),
    path('containers/edit/<int:container_id>', views.container_edit, name='container_edit'),
    path('edit-product/<int:product_id>', views.product_edit, name='product_edit'),
    path('warehouse/<int:warehouse_id>', views.warehouse_container_list, name='warehouse_containers_list'),
    path('warehouse/list', views.warehouse_list, name='warehouse_list'),
    path('report/day', views.calc_day, name='report-day')
]
