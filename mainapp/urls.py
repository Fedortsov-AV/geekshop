from django.urls import path
from mainapp.views import ProductView, ProductCategoryView


app_name = 'mainapp'

urlpatterns = [
    path('', ProductView.as_view(), name='index'),
    path('category/<int:pk>/', ProductCategoryView.as_view(), name='product'),
    path('page/<int:page>/', ProductView.as_view(), name='page'),
]