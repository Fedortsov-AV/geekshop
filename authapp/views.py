from django.shortcuts import render


def login(request):
    context = {'title': 'GeekShop - Авторизация'}
    return render(request, 'authapp/login.html', context)


def register(request):
    context = {'title': 'GeekShop - Регистрация'}
    return render(request, 'authapp/register.html', context)
