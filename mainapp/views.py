import json

from django.shortcuts import render
from mainapp.models import Product, ProductCategory


# Create your views here.


def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'mainapp/index.html', context)


def products(request):
    context = {
        'title': 'GeekShop - каталог',
        'products': Product.objects.all(),
        'category': ProductCategory.objects.all(),
    }

    return render(request, 'mainapp/products.html', context)
