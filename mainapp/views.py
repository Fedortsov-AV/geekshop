from django.shortcuts import render
from django.views.generic import ListView
from mainapp.models import Product, ProductCategory


# Create your views here.
def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'mainapp/index.html', context)


class ProductView(ListView):
    model = Product
    template_name = 'mainapp/products.html'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        context.update({'title': 'GeekShop - товары'})
        
        return context


class ProductCategoryView(ListView):
    model = Product
    template_name = 'mainapp/products.html'
    paginate_by = 3

    def get_queryset(self):
        return Product.objects.filter(category=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCategoryView, self).get_context_data(**kwargs)
        context.update({'title': 'GeekShop - товары'})

        return context
