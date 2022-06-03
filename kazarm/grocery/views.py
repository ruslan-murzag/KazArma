from django.shortcuts import render
from .models import *


def ProductList(request):
    products = Product.objects.all()
    f_s = First_stage.objects.all()

    return render(request,
                  'grocery/list.html',
                  {'products': products,
                   'f_s': f_s})
