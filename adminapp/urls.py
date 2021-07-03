from django.urls import path
from adminapp.views import index, OrderUpdateView
from adminapp.views import UserListView, UserCreateView, UserUpdateView, UserDeleteView, UserRestoryView,\
    ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView, OrderListView

app_name = "adminapp"

urlpatterns = [
    path('', index, name='index'),
    path('admin-users-read/', UserListView.as_view(), name='admin_users_read'),
    path('admin-users-create/', UserCreateView.as_view(), name='admin_users_create'),
    path('admin-users-update/<int:pk>/', UserUpdateView.as_view(), name='admin_users_update'),
    path('admin-user-remove/<int:pk>/', UserDeleteView.as_view(), name='admin_user_remove'),
    path('admin-user-restore/<int:pk>/', UserRestoryView.as_view(), name='admin_user_restore'),
    path('admin-products-read/', ProductListView.as_view(), name='admin_products_read'),
    path('admin-products-create/', ProductCreateView.as_view(), name='admin_products_create'),
    path('admin-products-update/<int:pk>/', ProductUpdateView.as_view(), name='admin_products_update'),
    path('admin-products-remove/<int:pk>/', ProductDeleteView.as_view(), name='admin_products_remove'),
    path('admin-order-read/', OrderListView.as_view(), name='admin_order_read'),
    path('admin-order-update/<pk>/', OrderUpdateView.as_view(), name='admin_order_update'),
]
