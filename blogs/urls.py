from django.urls import path
from . import views

app_name="blogs"

urlpatterns = [
    path('', views.blogs, name='blog_list'),
    path('category/<slug:category_slug>/', views.blogs, name='blog_list_category'),
    path('tag/<slug:tag_slug>/', views.blogs, name='blog_list_tag'),
    path('detail/<slug:blog_slug>/', views.blog_detail, name='blog_detail')
]