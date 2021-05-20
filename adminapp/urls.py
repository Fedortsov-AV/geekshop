from django.urls import path
from adminapp.views import index, admin_users_read, admin_users_create, admin_users_update, admin_user_remove, \
    admin_user_restore

app_name = "adminapp"

urlpatterns = [
    path('', index, name='index'),
    path('admin-users-read/', admin_users_read, name='admin_users_read'),
    path('admin-users-create/', admin_users_create, name='admin_users_create'),
    path('admin-users-update/<int:user_id>/', admin_users_update, name='admin_users_update'),
    path('admin-user-remove/<int:user_id>/', admin_user_remove, name='admin_user_remove'),
    path('admin-user-restore/<int:user_id>/', admin_user_restore, name='admin_user_restore'),

]
