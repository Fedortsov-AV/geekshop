from django.urls import path
from authapp.views import logout, edit
from authapp.views import Login, register, verify

app_name = "authapp"

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('profile/<pk>/', edit, name='profile'),
    path('verify/<email>/<key>/', verify, name='verify'),
]
