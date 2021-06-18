import logging

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import HttpResponseRedirect, render
from django.contrib import auth, messages
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


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            if send_verify_link(user):
                logging.debug('send successful')
            else:
                logging.error('send failed')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegisterForm()
    context = {'title': 'GeekShop - Регистрация', 'form': form}
    return render(request, 'authapp/register.html', context)


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


def send_verify_link(user):
    verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
    subject = 'Account verify'
    message = f'Your link for account activation: {settings.DOMAIN_NAME}{verify_link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, key):
    user = User.objects.filter(email=email).first()
    if user and user.activation_key == key and not user.is_activation_key_expire():
        user.is_active = True
        user.activation_key = ''
        user.activation_key_created = None
        user.save()
        Login.as_view(request)
    return render(request, 'authapp/verify.html')
