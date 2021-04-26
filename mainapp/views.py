import json

from django.shortcuts import render


# Create your views here.


def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'mainapp/index.html', context)


def products(request):
    context = {
    'title': 'GeekShop - каталог',
}
    context['products'] = []

    with open("mainapp/fixtures/products.json") as read_f:
        prod = json.load(read_f)
        for i in prod['products']:
            context['products'].append(i)
    return render(request, 'mainapp/products.html', context)
