from django.urls import path
from authapp.views import login


app_name = "auth"

urlpatterns = [
    path('login/', login, name='index'),
    # path('logout/', authapp.logout, name='logout'),
]
