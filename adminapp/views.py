from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.models import User
from adminapp.forms import UserAdminRegisterForm, UserAdminProfileForm, ProductAdminForm
from mainapp.models import Product


@user_passes_test(lambda u: u.is_superuser)
def admin_products_remove(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return HttpResponseRedirect(reverse('admin_staff:admin_products_read'))


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def admin_products_update(request, product_id):
    selected_product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ProductAdminForm(data=request.POST, instance=selected_product, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_staff:admin_products_read'))
    else:
        form = ProductAdminForm(instance=selected_product)

    context = {'form': form, 'selected_product': selected_product}
    return render(request, 'adminapp/admin-products-update-delete.html', context)


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def admin_products_read(request):
    context = {'products': Product.objects.all()}
    return render(request, "adminapp/admin-products-read.html", context)


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def admin_products_create(request):
    if request.method == 'POST':
        form = ProductAdminForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_staff:admin_products_read'))
    else:
        form = ProductAdminForm()
    context = {'form': form}
    return render(request, 'adminapp/admin-product-create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'adminapp/admin.html')


# CRUD - Create Read Update Delete
@user_passes_test(lambda u: u.is_superuser)
def admin_users_read(request):
    context = {'users': User.objects.all()}
    return render(request, 'adminapp/admin-users-read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_create(request):
    if request.method == 'POST':
        form = UserAdminRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_staff:admin_users_read'))
    else:
        form = UserAdminRegisterForm()
    context = {'form': form}
    return render(request, 'adminapp/admin-users-create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_update(request, user_id):
    selected_user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = UserAdminProfileForm(data=request.POST, instance=selected_user, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_staff:admin_users_read'))
    else:
        form = UserAdminProfileForm(instance=selected_user)

    context = {'form': form, 'selected_user': selected_user}
    return render(request, 'adminapp/admin-users-update-delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_user_remove(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return HttpResponseRedirect(reverse('admin_staff:admin_users_read'))


@user_passes_test(lambda u: u.is_superuser)
def admin_user_restore(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return HttpResponseRedirect(reverse('admin_staff:admin_users_read'))
