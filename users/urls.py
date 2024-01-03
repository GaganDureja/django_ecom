from django.urls import path
from . import views

app_name="users"

urlpatterns = [
    
    path('signup', views.Signup, name='Signup'),
    path('signin', views.Signin, name='Signin'),
    path('logout', views.user_logout, name='logout'),
    path('', views.users, name='users'),
    # path('', views.Home, name='home'),
]