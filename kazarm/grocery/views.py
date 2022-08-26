from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Product, First_stage, Container, Warehouse, Store, Tray
from .forms import *
from django.urls import reverse
from django.db.models import Avg, Count, Sum, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
import datetime
from .filters import TrayFilter, ArrivalFilter
from report.views import list_container


@login_required
def first_stage_list(request):
    today = datetime.datetime.today()
    products = Product.objects.all()
    f_s = First_stage.objects.all().order_by('-id')
    calc_mass = []
    different_mass = 0
    for i in products:
        all_obj = First_stage.objects.filter(created__day=today.day).filter(title=i)
        if all_obj:
            different_mass = all_obj.aggregate(Sum('first_m'))['first_m__sum'] - all_obj.aggregate(Sum('second_m'))[
                'second_m__sum']
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
                  {'post_form': product_form})


@login_required
def warehouse_container_list(request, warehouse_id):
    warehouse = get_object_or_404(Warehouse, id=warehouse_id)
    title = warehouse.title
    containers = warehouse.container.all().order_by('-id')
    containers = containers.filter(Q(status='Отходы') | Q(status='Склад'))
    paginator = Paginator(containers, 30)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)


    trays = Tray.objects.filter(status='Склад').filter(status1=' ').order_by('-id')

    paginator1 = Paginator(trays, 30)
    page1 = request.GET.get('page')
    try:
        posts1 = paginator1.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts1 = paginator1.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts1 = paginator1.page(paginator.num_pages)


    return render(request,
                  'grocery/warehouse/list_containers.html',
                  {'page': page,
                   'posts': posts,
                   'title': title,
                   'page1': page1,
                   'posts1': posts1
                   })


@login_required
def warehouse_list(request):
    warehouses = Warehouse.objects.all()
    table = []
    for i in warehouses:
        container_list = i.container.filter(status='Склад').filter(status1=' ')
        tray_list = i.tray.filter(status='Склад').filter(status1=' ')
        if container_list:
            container_mass = container_list.aggregate(Sum('mass1'))['mass1__sum'] - container_list.aggregate(Sum('box_mass1'))['box_mass1__sum']
        else:
            container_mass = 0

        if tray_list:
            tray_mass = tray_list.aggregate(Sum('mass1'))['mass1__sum'] - tray_list.aggregate(Sum('mass2'))['mass2__sum']
        else:
            tray_mass = 0

        tray_net = tray_list.filter(packing='Сетка')
        tray_bag = tray_list.filter(packing='Мешок')
        if tray_net:
            tray_net_num = tray_list.filter(packing='Сетка').aggregate(Sum('number_pr'))['number_pr__sum']
        else:
            tray_net_num = 0
        if tray_bag:
            tray_bag_num = tray_list.filter(packing='Мешок').aggregate(Sum('number_pr'))['number_pr__sum']
        else:
            tray_bag_num = 0

        table.append([i, container_mass, tray_mass, tray_net_num, tray_bag_num])

    paginator = Paginator(table, 30)
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
def containers_list_by_title(request, title):
    container_list = Container.objects.filter(title=title).order_by('-id')
    paginator = Paginator(container_list, 20)
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
                  'grocery/containers/list_by_title.html',
                  {'container_list': posts,
                   'page': page})


@login_required
def containers_list_by_date_create(request, year, month, day):
    container_list = Container.objects.filter(created__year=year, created__month=month, created__day=day).order_by('-id')
    date = datetime.datetime(year=year, month=month, day=day)

    return render(request,
                  'grocery/containers/list_by_date.html',
                  {'container_list': container_list,
                   'date': date})

@login_required
def containers_list_by_date_update(request, year, month, day):
    container_list = Container.objects.filter(updated__year=year, updated__month=month, updated__day=day).order_by(
        '-id')
    date = datetime.datetime(year=year, month=month, day=day)
    return render(request,
                  'grocery/containers/list_by_date_update.html',
                  {'container_list': container_list,
                   'date': date})
@login_required
def containers_list_by_status(request, num, status):
    if num == 1:
        container_list = Container.objects.filter(status=status).filter(status1=' ').order_by('-id')
    else:
        container_list = Container.objects.filter(status1=status).order_by('-id')

    paginator = Paginator(container_list, 20)
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
                  'grocery/containers/list_by_status.html',
                  {'container_list': posts,
                   'page': page,
                   'status': status})


@login_required
def arrival_by_date_create(request, year, month, day):
    arrivals_list = First_stage.objects.filter(created__year=year, created__month=month, created__day=day).order_by('-id')
    date = datetime.datetime(year=year, month=month, day=day)
    return render(request,
                  'grocery/first_stage/by_date_create.html',
                  {'arrivals_list': arrivals_list,
                   'date': date})


@login_required
def arrival_by_date_update(request, year, month, day):
    arrivals_list = First_stage.objects.filter(updated__year=year, updated__month=month, updated__day=day).order_by('-id')
    date = datetime.datetime(year=year, month=month, day=day)
    return render(request,
                  'grocery/first_stage/by_date_create.html',
                  {'arrivals_list': arrivals_list,
                   'date': date})


@login_required
def arrival_by_auto(request, auto):
    arrivals_list = First_stage.objects.filter(numbers_auto=auto).order_by('-id')

    paginator = Paginator(arrivals_list, 20)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'grocery/first_stage/by_auto.html',
                  {'arrivals_list': posts,
                   'page': page,
                   'auto': auto})


@login_required
def arrival_by_title(request, title):
    arrivals_list = First_stage.objects.filter(title=title).order_by('-id')
    paginator = Paginator(arrivals_list, 20)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    print(arrivals_list)
    print('Hello')
    return render(request, 'grocery/first_stage/by_title.html',
                  {'arrivals_list': posts,
                   'page': page,
                   'title': title})


@login_required
def list_trays(request):
    trays_list = Tray.objects.all().order_by('-id')
    paginator = Paginator(trays_list, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'grocery/trays/list.html', {'page': page, 'posts': posts})


@login_required
def tray_create(request):
    if request.method == 'POST':
        add_type_product = tray_create_form(data=request.POST)
        if add_type_product.is_valid():
            add_type_product = add_type_product.save(commit=False)
            add_type_product.save()
            return HttpResponseRedirect(reverse('grocery:trays_list'))
    else:
        add_type_product = tray_create_form()

    return render(request, 'grocery/trays/tray_create.html', {
        'post_form': add_type_product,
    })


@login_required
def tray_filter(request):
    tray = Tray.objects.all().order_by('-id')
    myFilter = TrayFilter(request.GET, queryset=tray)
    paginator = Paginator(myFilter.qs, 10)

    table = tray_table(myFilter.qs)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'filter/filter_tray_page.html', {'page': page, 'myFilter': myFilter, 'posts': posts, 'table': table})


def tray_table(trays):
    product_list = Product.objects.all()
    table = []
    for i in product_list:
        trays_list = trays.filter(title=i)
        if trays_list:
            netto = trays_list.aggregate(Sum('mass1'))['mass1__sum'] - trays_list.aggregate(Sum('mass2'))['mass2__sum']
            bag = trays_list.filter(packing='Мешок')
            net = trays_list.filter(packing='Сетка')
            if bag:
                type1 = bag.aggregate(Sum('number_pr'))['number_pr__sum']
            else:
                type1 = 0
            if net:
                type2 = net.aggregate(Sum('number_pr'))['number_pr__sum']
            else:
                type2 = 0

            sum_type = type2 + type1
        else:
            netto = 0
            type1 = 0
            type2 = 0
            sum_type = 0
        table.append([i, netto, type1, type2, sum_type])
    return table



@login_required
def tray_edit(request, id):
    trays = get_object_or_404(Tray, id=id)

    if request.method == 'POST':
        product_form = tray_edit_form(data=request.POST, instance=trays)

        if product_form.is_valid():
            product_form = product_form.save(commit=False)
            product_form.save()
            return HttpResponseRedirect(reverse('grocery:trays_list'))
    else:
        product_form = tray_edit_form(instance=trays)

    return render(request,
                  'grocery/trays/tray_edit.html',
                  {'post_form': product_form})


@login_required
def arrival_filter(request):
    arrivals = First_stage.objects.all().order_by('-id')
    myFilter = ArrivalFilter(request.GET, queryset=arrivals)
    paginator = Paginator(myFilter.qs, 10)

    products = Product.objects.all()
    calc_mass = []
    different_mass = 0
    for i in products:
        all_obj = myFilter.qs.filter(title=i)
        if all_obj:
            different_mass = all_obj.aggregate(Sum('first_m'))['first_m__sum'] - all_obj.aggregate(Sum('second_m'))[
                'second_m__sum']
        else:
            different_mass = 0
        calc_mass.append([i.title, different_mass])

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'filter/filter_arrival_page.html', {'page': page, 'myFilter': myFilter, 'posts': posts, 'table': calc_mass})

