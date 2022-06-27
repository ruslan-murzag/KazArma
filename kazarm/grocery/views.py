from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Product, First_stage, Container, Warehouse
from .forms import *
from django.urls import reverse
from django.db.models import Avg, Count, Sum, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
import datetime

@login_required
def first_stage_list(request):

    products = Product.objects.all()
    f_s = First_stage.objects.all().order_by('-id')
    calc_mass = []
    different_mass = 0
    for i in products:
        all_obj = First_stage.objects.filter(title=i)
        if all_obj:
            different_mass = all_obj.aggregate(Sum('first_m'))['first_m__sum'] - all_obj.aggregate(Sum('second_m'))['second_m__sum']
        else:
            different_mass = 0
        calc_mass.append(different_mass)

    paginator = Paginator(f_s, 50)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)


    product_mass = dict(zip(products, calc_mass))
    return render(request,
                  'grocery/first_stage/main.html',
                  {'products': products,
                   'page': page,
                   'product_mass': product_mass.items(),
                   'f_s': posts})


@login_required
def first_stage_create(request):
    if request.method == 'POST':
        create_product = first_stage_form(data=request.POST)
        if create_product.is_valid():
            create_post_form = create_product.save(commit=False)
            create_post_form.save()
            return HttpResponseRedirect(reverse('grocery:product-list'))
    else:
        create_post_form = first_stage_form()

    return render(request, 'grocery/first_stage/add_item.html', {
        'post_form': create_post_form,
    })


@login_required
def first_stage_edit(request, f_s_id):
    post = get_object_or_404(First_stage, id=f_s_id)
    if request.method == 'POST':
        post_form = first_stage_edit_form(data=request.POST, instance=post)

        if post_form.is_valid():
            post_form = post_form.save(commit=False)
            post_form.save()
            return HttpResponseRedirect(reverse('grocery:product-list'))
    else:
        post_form = first_stage_edit_form(instance=post)

    return render(request,
                  'grocery/first_stage/edit_item.html',
                  {'post_form': post_form})

@login_required
def product_create(request):
    if request.method == 'POST':
        add_type_product = product_add_form(data=request.POST)
        if add_type_product.is_valid():
            add_type_product = add_type_product.save(commit=False)
            add_type_product.save()
            return HttpResponseRedirect(reverse('grocery:product-list'))
    else:
        add_type_product = product_add_form()

    return render(request, 'grocery/first_stage/add_product.html', {
        'post_form': add_type_product,
    })


@login_required
def container_list(request):
    containers = Container.objects.all().order_by('-id')

    paginator = Paginator(containers, 50)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'grocery/containers/list.html',
                  {'page': page,
                   'posts': posts
                   })


@login_required
def container_create(request):
    if request.method == 'POST':
        create_container = container_create_form(data=request.POST)
        if create_container.is_valid():
            create_container = create_container.save(commit=False)
            create_container.save()
            return HttpResponseRedirect(reverse('grocery:containers_list'))
    else:
        create_container = container_create_form()

    return render(request, 'grocery/containers/add_item.html', {
        'post_form': create_container,
    })


@login_required
def container_edit(request, container_id):
    container = get_object_or_404(Container, id=container_id)
    if request.method == 'POST':
        container_form = container_edit_form(data=request.POST, instance=container)

        if container_form.is_valid():
            container_form = container_form.save(commit=False)
            container_form.save()
            return HttpResponseRedirect(reverse('grocery:containers_list'))
    else:
        container_form = container_edit_form(instance=container)

    return render(request,
                  'grocery/containers/edit_item.html',
                  {'post_form': container_form})


@login_required
def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product_form = product_edit_form(data=request.POST, instance=product)

        if product_form.is_valid():
            product_form = product_form.save(commit=False)
            product_form.save()
            return HttpResponseRedirect(reverse('grocery:product-list'))
    else:
        product_form = product_edit_form(instance=product)

    return render(request,
                  'grocery/first_stage/edit_product.html',
                  {'post_form':product_form})


@login_required
def warehouse_container_list(request, warehouse_id):
    warehouse = get_object_or_404(Warehouse, id=warehouse_id)
    title = warehouse.title
    containers = warehouse.container.all().order_by('-id')
    paginator = Paginator(containers, 50)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'grocery/warehouse/list_containers.html',
                  {'page': page,
                   'posts': posts,
                   'title': title
                   })


@login_required
def warehouse_list(request):
    warehouses = Warehouse.objects.all()
    paginator = Paginator(warehouses, 30)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'grocery/warehouse/list_warehouse.html',
                  {'page': page,
                   'posts': posts})


@login_required
def calc_day(request):
    today = datetime.datetime.today()
    data_list1 = []
    data_list2 = []
    prods = Product.objects.all()
    for i in range(0, 7):
        data = today - datetime.timedelta(days=i)
        f_s_obj = First_stage.objects.all().filter(created__day=data.day)
        containers_obj = Container.objects.all().filter(created__day=data.day).filter(Q(status='Склад') | Q(status='Отходы'))
        if containers_obj:
            m1 = containers_obj.aggregate(Sum('mass1'))['mass1__sum'] - containers_obj.aggregate(Sum('box_mass1'))['box_mass1__sum']
        else:
            m1 = 0
        if f_s_obj:
            m2 = f_s_obj.aggregate(Sum('first_m'))['first_m__sum'] - f_s_obj.aggregate(Sum('second_m'))['second_m__sum']
        else:
            m2 = 0

        among_cont = len(containers_obj)
        among_f_s = len(f_s_obj)
        data_list1.append([data, m1, m2, among_cont, among_f_s])

        containers_sail = Container.objects.all().filter(created__day=data.day).filter(status='Продажа')
        containers_sort = Container.objects.all().filter(created__day=data.day).filter(status='Сортировка')
        if containers_sort:
            netto2 = containers_sort.aggregate(Sum('mass2'))['mass2__sum'] - containers_sort.aggregate(Sum('box_mass2'))['box_mass2__sum']
            nett2_1 = containers_sort.aggregate(Sum('mass1'))['mass1__sum'] - containers_sort.aggregate(Sum('box_mass1'))['box_mass1__sum']
            different_1 = netto2 - nett2_1
        else:
            netto2 = 0
            different_1 = 0
        if containers_sail:
            netto1 = containers_sail.aggregate(Sum('mass1'))['mass1__sum'] - containers_sail.aggregate(Sum('box_mass1'))['box_mass1__sum']
            different_2 =  netto1 - netto2
        else:
            netto1 = 0
            different_2 = 0


        data_list2.append([data, netto2, different_1, netto1, different_2])
    return render(request,
                  'grocery/time_report/day.html',
                  {'data_list1': data_list1,
                   'data_list2': data_list2,
                   })