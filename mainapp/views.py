from django.shortcuts import render
from mainapp.models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'mainapp/index.html', context)


def products(request, category_id=None, page=1):
    context = {
        'title': 'GeekShop - каталог',
        'category': ProductCategory.objects.all(),
    }
    product = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    paginator = Paginator(product, per_page=3)
    try:
        product_paginator = paginator.page(page)
    except PageNotAnInteger:
        product_paginator = paginator.page(1)
    except EmptyPage:
        product_paginator = paginator.page(paginator.num_pages)
    context.update({'products': product_paginator})
    return render(request, 'mainapp/products.html', context)
