import django_filters
from django import forms
from django.forms import SelectMultiple

from grocery.models import *
from django_filters import DateFilter


class ContainerFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        super(ContainerFilter, self).__init__(*args, **kwargs)
        self.filters['title'].label = 'Продукт'
        self.filters['status'].label = ' Первый Статус'
        self.filters['status1'].label = 'Второй Статус'
        self.filters['warehouse'].label = 'Склад'

    start_date = DateFilter(label='Создан от', field_name='created', lookup_expr='gte')
    end_date = DateFilter(label='Создан до', field_name='created', lookup_expr='lte')

    start_date1 = DateFilter(label='Изменен от', field_name='updated', lookup_expr='gte')
    end_date1 = DateFilter(label='Изменен до', field_name='updated', lookup_expr='lte')

    class Meta:
        model = Container
        fields = ('title', 'status', 'status1', 'warehouse', 'start_date', 'end_date', 'start_date1', 'end_date1')


