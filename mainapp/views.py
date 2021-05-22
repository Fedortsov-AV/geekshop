import json

from django.shortcuts import render
from mainapp.models import Product, ProductCategory


# Create your views here.


def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'mainapp/index.html', context)


def products(request, category_id=None):
    context = {
        'title': 'GeekShop - каталог',
        'category': ProductCategory.objects.all(),
    }
    if category_id:
        product = Product.objects.filter(category_id=category_id)
        context.update({'products': product})
    else:
        context.update({'products': Product.objects.all()})

    return render(request, 'mainapp/products.html', context)
