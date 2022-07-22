from django import forms
from .models import First_stage, Product, Container


class first_stage_form(forms.ModelForm):
    class Meta:
        model = First_stage
        fields = ('title', 'numbers_auto', 'first_m', 'second_m')
        labels = {
            'title': ('Название продукта'),
            'numbers_auto': ('Номер машины'),
            'first_m': ('Первый груз вес'),
            'second_m': ('Второй груз вес')
        }


class first_stage_edit_form(forms.ModelForm):
    class Meta:
        model = First_stage
        fields = ('title', 'numbers_auto', 'first_m', 'second_m')
        labels = {
            'title': ('Название продукта'),
            'numbers_auto': ('Номер машины'),
            'first_m': ('Первый груз вес'),
            'second_m': ('Второй груз вес')
        }


class product_add_form(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title',)
        labels = {
            'title': ('Название продукта')
        }


class container_create_form(forms.ModelForm):
    class Meta:
        model = Container
        fields = ('title', 'mass1',  'box_mass1', 'status', 'warehouse', 'mass2', 'box_mass2', 'stores')
        labels = {
            'title': ('Название продукта'),
            'mass1':('Масса1'),
            'status': ('Статус'),
            'warehouse': ('Место'),
            'mass2': ('Масса2'),
            'box_mass1':('Первая масса бокса'),
            'box_mass2':('Вторая масса бокса'),
            'stores': ('место отгрузки')
        }


class container_edit_form(forms.ModelForm):
    class Meta:
        model = Container
        fields = ('title', 'mass1',  'box_mass1',  'status', 'warehouse', 'mass2', 'box_mass2', 'stores')
        labels = {
            'title': ('Название продукта'),
            'mass1':('Масса1'),
            'status': ('Статус'),
            'warehouse': ('Место'),
            'mass2': ('Масса2'),
            'box_mass1':('Первая масса бокса'),
            'box_mass2':('Вторая масса бокса'),
            'stores': ('место отгрузки')
        }


class product_edit_form(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title',)
        labels = {'title': 'Название'}