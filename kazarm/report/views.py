from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import Avg, Count, Sum, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
import datetime
from grocery.models import *
from .filters import ContainerFilter

@login_required
def report(request, year, month, day):
    container_list = Container.objects.filter(created__year=year, created__month=month, created__day=day).filter(
        status='Отгружено')
    product_list = Product.objects.all()
    store_list = Store.objects.all()
    data_list = []
    date = datetime.datetime(year=year, month=month, day=day)
    for i in product_list:
        items = container_list.filter(title=i)
        if items:
            netto = items.aggregate(Sum('mass1'))['mass1__sum'] - items.aggregate(Sum('box_mass1'))['box_mass1__sum']
        else:
            netto = 0
        data_list.append([i, netto, items])

    date_list2 = []
    for i in store_list:
        store_item = container_list.filter(stores=i)
        if store_item:
            date_list2.append([i, len(store_item)])

    return render(request,
                  'time_report/report.html',
                  {'data_list': data_list,
                   'data_list2': date_list2,
                   'date': date})


@login_required
def stores(request):
    stores = Store.objects.all()
    return render(request,
                  'grocery/stores/stores.html',
                  {'stores': stores})


@login_required
def report_store(request, id):
    store = get_object_or_404(Store, id=id)
    store_trays = store.tray.all().order_by('-id')

    paginator = Paginator(store_trays, 20)
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
                  'grocery/stores/store_report.html',
                  {'posts': posts,
                   'page': page,
                   'store': store})


@login_required
def calc_day(request):
    today = datetime.datetime.today()
    data_list1 = []
    data_list2 = []

    prods = Product.objects.all()
    container_list = Container.objects.all()
    for i in range(0, 7):
        data = today - datetime.timedelta(days=i)
        f_s_obj = First_stage.objects.all().filter(created__year=data.year, created__month=data.month, created__day=data.day)
        containers_obj = container_list.filter(created__year=data.year, created__month=data.month, created__day=data.day).filter(Q(status='Склад'))
        containers_trash = container_list.filter(created__year=data.year, created__month=data.month, created__day=data.day).filter(Q(status='Отходы'))
        if containers_obj:
            m1 = containers_obj.aggregate(Sum('mass1'))['mass1__sum'] - containers_obj.aggregate(Sum('box_mass1'))[
                'box_mass1__sum']
        else:
            m1 = 0
        if f_s_obj:
            m2 = f_s_obj.aggregate(Sum('first_m'))['first_m__sum'] - f_s_obj.aggregate(Sum('second_m'))['second_m__sum']
        else:
            m2 = 0
        if containers_trash:
            m_trash = containers_trash.aggregate(Sum('mass1'))['mass1__sum'] - containers_trash.aggregate(Sum('box_mass1'))[
                'box_mass1__sum']
        else:
            m_trash = 0
        diff_m1_m2_trash = m1 - m2 + m_trash
        among_cont = len(containers_obj)
        among_f_s = len(f_s_obj)
        data_list1.append([data, m1, m2, m_trash, diff_m1_m2_trash, among_cont, among_f_s])

        trays = Tray.objects.all()
        containers_sort = container_list.filter(updated__year=data.year, updated__month=data.month, updated__day=data.day).filter(status1='Сортировка')
        trays = trays.filter(created__year=data.year, created__month=data.month, created__day=data.day).filter(status='Склад')
        if containers_sort:
            netto2 = containers_sort.aggregate(Sum('mass2'))['mass2__sum'] - \
                     containers_sort.aggregate(Sum('box_mass2'))['box_mass2__sum']
            nett2_1 = containers_sort.aggregate(Sum('mass1'))['mass1__sum'] - \
                      containers_sort.aggregate(Sum('box_mass1'))['box_mass1__sum']
            different_1 = netto2 - nett2_1
        else:
            netto2 = 0
            different_1 = 0
        if trays:
            trays_netto = trays.aggregate(Sum('mass1'))['mass1__sum'] - trays.aggregate(Sum('mass2'))['mass2__sum']
        else:
            trays_netto = 0
        data_list2.append([data, netto2, different_1, trays_netto, trays_netto - netto2])

    return render(request,
                  'time_report/day.html',
                  {'data_list1': data_list1,
                   'data_list2': data_list2,
                   })


@login_required
def first_stage_day_report(request, year, month, day):
    container_list = Container.objects.filter(created__year=year, created__month=month, created__day=day).filter(Q(status='Отходы') | Q(status='Склад')).order_by('-id')
    arrivals = First_stage.objects.filter(created__year=year, created__month=month, created__day=day).order_by('-id')
    date = datetime.datetime(year=year, month=month, day=day)

    products_list = Product.objects.all()
    product_calc = []
    arrivals_calc = []
    for i in products_list:
        items = container_list.filter(title=i)
        if items:
            netto = items.aggregate(Sum('mass1'))['mass1__sum'] - items.aggregate(Sum('box_mass1'))['box_mass1__sum']
        else:
            netto = 0
        product_calc.append([i, netto])

    for i in products_list:
        items = arrivals.filter(title=i)
        if items:
            netto = items.aggregate(Sum('first_m'))['first_m__sum'] - items.aggregate(Sum('second_m'))[
                'second_m__sum']
        else:
            netto = 0
        arrivals_calc.append([i, netto])

    return render(request, 'time_report/first_stage_day_report.html',
                  {'container_list': container_list,
                   'arrivals': arrivals,
                   'date': date,
                   'product_calc': product_calc,
                   'arrivals_calc': arrivals_calc})


@login_required
def second_stage_day_report(request, year, month, day):
    container_list = Container.objects.filter(updated__year=year, updated__month=month, updated__day=day).order_by('-id')
    container_list_sort = container_list.filter(status1='Сортировка')
    date = datetime.datetime(year=year, month=month, day=day)
    product_list = Product.objects.all()
    product_sort_calc = []
    trays_product_calc = []
    tray_list = Tray.objects.filter(created__year=year, created__month=month, created__day=day).filter(status='Склад')

    for i in product_list:
        items1 = container_list_sort.filter(title=i)
        if items1:
            netto1 = items1.aggregate(Sum('mass1'))['mass1__sum'] - items1.aggregate(Sum('box_mass1'))['box_mass1__sum']
            netto2 = items1.aggregate(Sum('mass2'))['mass2__sum'] - items1.aggregate(Sum('box_mass2'))['box_mass2__sum']
            diff1 = netto2 - netto1
        else:
            netto1 = 0
            netto2 = 0
            diff1 = 0
        product_sort_calc.append([i, netto1, netto2, diff1])

        items2 = tray_list.filter(title=i)
        if items2:
            netto1 = items2.aggregate(Sum('mass1'))['mass1__sum'] - items2.aggregate(Sum('mass2'))['mass2__sum']
        else:
            netto1 = 0
        trays_product_calc.append([i.title, netto1])
    return render(request,
                  'time_report/second_stage_day_report.html',

                  {'container_list_sort': container_list_sort,
                   'date': date,
                   'product_sort_calc': product_sort_calc,
                   'tray_list': tray_list,
                   'trays_product_calc': trays_product_calc})


@login_required
def filter_page(request):
    container_list = Container.objects.all().order_by('-id')
    myFilter = ContainerFilter(request.GET, queryset=container_list)

    table = list_container(myFilter.qs)

    paginator = Paginator(myFilter.qs, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'filter/filter_container_page.html', {'page': page, 'myFilter': myFilter, 'posts': posts, 'table': table})


def list_container(models):
    table_data = []
    products = Product.objects.all()
    for i in products:
        containers = models.filter(title=i)
        if containers:
            m1 = containers.aggregate(Sum('mass1'))['mass1__sum'] - containers.aggregate(Sum('box_mass1'))['box_mass1__sum']
            m2 = containers.aggregate(Sum('mass2'))['mass2__sum'] - containers.aggregate(Sum('box_mass2'))['box_mass2__sum']
            table_data.append([i, m1, m2])
        else:
            table_data.append([i, 0, 0])
    return table_data

