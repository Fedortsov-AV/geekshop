from django.urls import path
from basketapp.views import basket_edit, UserBasketAddView, UserBasketDeleteView

app_name = "basketapp"

urlpatterns = [
    path('add/<int:product_id>/', UserBasketAddView.as_view(), name='basket_add'),
    path('remove/<int:pk>/', UserBasketDeleteView.as_view(), name='basket_remove'),
    path('edit/<int:id>/<int:quantity>/', basket_edit, name='basket_edit'),
]
