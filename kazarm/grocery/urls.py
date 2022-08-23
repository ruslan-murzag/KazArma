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

    path('containers/<int:title>', views.containers_list_by_title, name='containers_list_by_title'),


    path('containers/list/date/<int:year>/<int:month>/<int:day>', views.containers_list_by_date_create, name='containers_list_by_date'),
    path('containers/list/date/update/<int:year>/<int:month>/<int:day>', views.containers_list_by_date_update,
         name='containers_list_by_date_update'),

    path('containers/list/status/<int:num>/<str:status>', views.containers_list_by_status, name='containers_list_by_status'),

    path('arrivals/date/create/<int:year>/<int:month>/<int:day>', views.arrival_by_date_create, name='arrivals_date_create'),
    path('arrivals/date/update/<int:year>/<int:month>/<int:day>', views.arrival_by_date_update,
         name='arrivals_date_update'),
    path('arrivals/<str:auto>', views.arrival_by_auto, name='arrivals_by_auto'),
    path('arrivals/title/<str:title>', views.arrival_by_title, name='arrivals_by_title'),


    path('trays/', views.list_trays, name='trays_list'),
    path('trays/create/', views.tray_create, name='tray_create'),
    path('trays/filter/', views.tray_filter, name='tray_filter'),
    path('trays/edit/<int:id>', views.tray_edit, name='tray_edit')
]
