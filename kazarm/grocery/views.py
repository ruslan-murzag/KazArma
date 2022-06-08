from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *
from django.urls import reverse
from django.db.models import Avg, Count, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


@login_required
def first_stage_list(request):

    products = Product.objects.all()
    f_s = First_stage.objects.all().order_by('-id')
    calc_mass = []
    different_mass = 0
    for i in products:
        all_obj = First_stage.objects.filter(title=i)
        if all_obj:
            different_mass = list(all_obj.aggregate(Sum('first_m')).values())[0] - list(all_obj.aggregate(Sum('second_m')).values())[0]
        else:
            different_mass = 0
        calc_mass.append(different_mass)

    paginator = Paginator(f_s, 100)
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
    if list(request.user.groups.all())[0].name == 'Админ':
        print('He is admin')
    else:
        print('Not admin')
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
