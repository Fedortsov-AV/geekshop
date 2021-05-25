from django.shortcuts import HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView
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


class ProfileView(UpdateView):
    model = User
    template_name = 'authapp/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('index')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update({'title': 'GeekShop - Профиль пользователя ' + str(User.objects.get(id=self.kwargs['pk']))})
        context.update({'baskets': Basket.objects.filter(user=self.kwargs['pk'])})
        return context


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
