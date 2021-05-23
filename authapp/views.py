from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from basketapp.models import Basket
from authapp.models import User


class Login(LoginView):
    module = User
    template_name = 'authapp/login.html'
    success_url = reverse_lazy('index')
    form_class = UserLoginForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Login, self).get_context_data(**kwargs)
        context.update({'title': 'GeekShop - Авторизация'})
        return context


class Register(CreateView):
    model = User
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('authapp:login')
    form_class = UserRegisterForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Register, self).get_context_data(**kwargs)
        context.update({'title': 'GeekShop - Регистрация'})
        return context


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'title': 'GeekShop - личный кабинет',
        'form': form,
        'baskets': Basket.objects.filter(user=request.user),

    }
    return render(request, 'authapp/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
