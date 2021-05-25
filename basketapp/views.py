from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, DeleteView
from django.http import JsonResponse
from django.urls import reverse_lazy

from mainapp.models import Product
from basketapp.models import Basket


class UserBasketAddView(UpdateView):
    model = Basket
    success_url = reverse_lazy('HTTP_REFERER')

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs['product_id'])
        baskets = Basket.objects.filter(user=self.request.user, product=product)
        if not baskets.exists():
            basket = Basket.objects.create(user=self.request.user, product=product, quantity=1)
            basket.save()
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserBasketAddView, self).dispatch(request, *args, **kwargs)


class UserBasketDeleteView(DeleteView):
    model = Basket

    def get(self, request, *args, **kwargs):
        basket = Basket.objects.get(id=self.kwargs['pk'])
        basket.delete()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserBasketDeleteView, self).dispatch(request, *args, **kwargs)


def basket_edit(request, id, quantity):
    if request.is_ajax():
        basket = Basket.objects.get(id=id)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()
        baskets = Basket.objects.filter(user=request.user)
        context = {
            'baskets': baskets
        }
        result = render_to_string('basketapp/basket.html', context)
        return JsonResponse({'result': result})
