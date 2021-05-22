from django.urls import path
from adminapp.views import index, admin_user_restore, admin_products_read, admin_products_create, admin_products_update, admin_products_remove
from adminapp.views import UserListView, UserCreateView, UserUpdateView, UserDeleteView, UserRestoryView

app_name = "adminapp"

urlpatterns = [
    path('', index, name='index'),
    path('admin-users-read/', UserListView.as_view(), name='admin_users_read'),
    path('admin-users-create/', UserCreateView.as_view(), name='admin_users_create'),
    path('admin-users-update/<int:pk>/', UserUpdateView.as_view(), name='admin_users_update'),
    path('admin-user-remove/<int:pk>/', UserDeleteView.as_view(), name='admin_user_remove'),
    path('admin-user-restore/<int:pk>/', UserRestoryView.as_view(), name='admin_user_restore'),
    path('admin-products-read/', admin_products_read, name='admin_products_read'),
    path('admin-products-create/', admin_products_create, name='admin_products_create'),
    path('admin-products-update/<int:product_id>/', admin_products_update, name='admin_products_update'),
    path('admin-products-remove/<int:product_id>/', admin_products_remove, name='admin_products_remove'),

]
