import logging

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.views.generic import DetailView
from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm
from basketapp.models import Basket
from authapp.models import User, UserProfile


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


def edit(request, **kwargs):
    title = 'GeekShop - Профиль пользователя ' + str(User.objects.get(id=request.user.pk))
    if request.method == 'POST':
        profile_form = UserProfileEditForm(request.POST, request.FILES, instance=request.user)
        edit_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('authapp:profile', args=[request.user.pk]))

    else:
        edit_form = UserProfileForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.userprofile)

    content = {
        'title': title,
        'baskets': Basket.objects.filter(user=request.user.pk),
        'form': edit_form,
        'profile_form': profile_form
    }
    return render(request, 'authapp/profile.html', content)


# class ProfileView(UpdateView):
#     model = User
#     template_name = 'authapp/profile.html'
#     form_class = UserProfileForm
#     success_url = reverse_lazy('index')
#
#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({'title': 'GeekShop - Профиль пользователя ' + str(User.objects.get(id=self.kwargs['pk']))})
#         context.update({'baskets': Basket.objects.filter(user=self.kwargs['pk'])})
#         profile_form = UserProfileEditForm(instance=self.request.user.userprofile)
#         context.update({'profile_form': profile_form})
#         return context
#
#     def post(self, request, *args, **kwargs):
#         user_form = UserProfileForm(request.POST, instance=self.request.user)
#         profile_form = UserProfileEditForm(request.POST, instance=UserProfile.objects.get(user=self.request.user))
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             messages.success(self.request, "Your profile was updated.")
#             return redirect(reverse('index'))
#         else:
#             return super(ProfileView, self).get(request, *args, **kwargs)


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
        Login.as_view()
    return HttpResponseRedirect(reverse('index'))
