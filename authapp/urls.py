from django.urls import path
from authapp.views import logout
from authapp.views import Login, Register, ProfileView


app_name = "authapp"

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', logout, name='logout'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
   ]
