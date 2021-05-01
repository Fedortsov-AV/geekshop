from django.shortcuts import render


def login(request):
    context = {'title': 'GeekShop - Autorisation'}
    return render(request, 'authapp/login.html', context)
