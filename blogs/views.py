from django.shortcuts import render, get_object_or_404
from .models import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def top_blogs(request):
    t_blogs = Blog.objects.all().order_by('-id')[:4]
    return t_blogs


def blogs(request, category_slug=None, tag_slug=None):
    all_blogs = Blog.objects.all()
    
    cat = None
    tag_slug = None
    
    if category_slug:
        cat = get_object_or_404(Category, slug=category_slug)
        all_blogs = all_blogs.filter(category=cat)


    if tag_slug:
        subcat = get_object_or_404(Tag, slug=tag_slug)
        all_blogs = all_blogs.filter(sub_category=subcat)

    
    page = request.GET.get('page', 1)
    paginator = Paginator(all_blogs, 6)
    
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    return render(request, 'blogs/blogs.html', {'all_blogs': blogs})



def blog_detail(request, blog_slug):
    blog_det = get_object_or_404(Blog, slug=blog_slug)
    return render(request, 'blogs/blog-detail.html',{'blog_det':blog_det})