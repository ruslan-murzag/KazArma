import django_filters
from django import forms
from django.forms import SelectMultiple

from .models import *
from django_filters import DateFilter


class TrayFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        super(TrayFilter, self).__init__(*args, **kwargs)
        self.filters['title'].label = 'Продукт'
        self.filters['status'].label = 'Статус 1'
        self.filters['status1'].label = 'Статус 2'
        self.filters['warehouse'].label = 'Склад'

    start_date = DateFilter(label='Создан от', field_name='created', lookup_expr='gte')
    end_date = DateFilter(label='Создан до', field_name='created', lookup_expr='lte')

    start_date1 = DateFilter(label='Изменен от', field_name='updated', lookup_expr='gte')
    end_date1 = DateFilter(label='Изменен до', field_name='updated', lookup_expr='lte')

    class Meta:
        model = Tray
        fields = ('title', 'status', 'status1', 'warehouse', 'start_date', 'end_date', 'start_date1', 'end_date1')


class ArrivalFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        super(ArrivalFilter, self).__init__(*args, **kwargs)
        self.filters['title'].label = 'Продукт'
        self.filters['numbers_auto'].label = 'Номер машины'

    start_date = DateFilter(label='Создан от', field_name='created', lookup_expr='gte')
    end_date = DateFilter(label='Создан до', field_name='created', lookup_expr='lte')

    start_date1 = DateFilter(label='Изменен от', field_name='updated', lookup_expr='gte')
    end_date1 = DateFilter(label='Изменен до', field_name='updated', lookup_expr='lte')

    class Meta:
        model = First_stage
        fields = ('title', 'numbers_auto')
