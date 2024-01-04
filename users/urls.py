from django.urls import path
from . import views

app_name="users"

urlpatterns = [
    path('', views.users, name='users'),
    path('signup', views.Signup, name='Signup'),
    path('signin', views.Signin, name='Signin'),
    path('logout', views.user_logout, name='logout'),
    
    # path('', views.Home, name='home'),
]