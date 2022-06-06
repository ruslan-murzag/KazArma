from django import forms
from .models import First_stage, Product


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


class product_add_form(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title',)
