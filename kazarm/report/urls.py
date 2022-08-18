from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'report'


urlpatterns = [
    path('day', views.calc_day, name='report-day'),

    path('store/<int:id>', views.report_store, name='report_store'),
    path('stores/', views.stores, name='stores'),

    path('<int:year>/<int:month>/<int:day>', views.report, name='report'),

    path('first_stage_day/<int:year>/<int:month>/<int:day>', views.first_stage_day_report,
         name='first_day_report'),
    path('second_stage_day/<int:year>/<int:month>/<int:day>', views.second_stage_day_report,
         name='second_day_report'),


    path('filter_page/', views.filter_page, name='filter_page')

]
