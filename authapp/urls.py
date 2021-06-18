from django.urls import path
from authapp.views import logout
from authapp.views import Login, register, ProfileView, verify


app_name = "authapp"

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('profile/<pk>/', ProfileView.as_view(), name='profile'),
    path('verify/<email>/<key>/', verify, name='verify'),
   ]
