from django import forms
from .models import First_stage, Product, Container, Tray


class first_stage_form(forms.ModelForm):
    class Meta:
        model = First_stage
        fields = ('title', 'numbers_auto', 'first_m', 'second_m')
        labels = {
            'title': ('Название продукта'),
            'numbers_auto': ('Номер машины'),
            'first_m': ('Вес груженной машины'),
            'second_m': ('Вес машины')
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
        fields = ('title', 'mass1',  'box_mass1', 'status', 'warehouse')
        labels = {
            'title': ('Название продукта'),
            'mass1':('Вес продукта с тарой'),
            'status': ('Статус'),
            'warehouse': ('Место'),
            # 'mass2': ('Масса2'),
            'box_mass1':('Вес тары'),
            # 'box_mass2':('Вторая масса бокса'),
            # 'stores': ('место отгрузки')
        }


class container_edit_form(forms.ModelForm):
    class Meta:
        model = Container
        fields = ('status1', 'mass2', 'box_mass2', 'stores')
        labels = {
            'title': ('Название продукта'),
            'mass1':('Вес продукта с тарой'),
            'status1': ('Статус'),
            'warehouse': ('Место'),
            'mass2': ('Вес продукта с тарой'),
            'box_mass1':('Вес тары'),
            'box_mass2':('Вес тары'),
            'stores': ('место отгрузки')
        }


class product_edit_form(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title',)
        labels = {'title': 'Название'}


class tray_create_form(forms.ModelForm):
    class Meta:
        model = Tray
        fields = ('title', 'status', 'mass1', 'mass2', 'packing', 'warehouse', 'number_pr', 'stores')
        labels = {
            'title': ('Название продукта'),
            'mass1': ('Вес продукта с поддоном'),
            'mass2': ('Вес поддона'),
            'status1': ('Статус'),
            'status': ('Статус'),
            'warehouse': ('Место'),
            'packing': ('тип фасовки'),
            'number_pr': ('количество'),
            'stores': ('место отгрузки')
        }


class tray_edit_form(forms.ModelForm):
    class Meta:
        model = Tray
        fields = ('status1', 'stores')