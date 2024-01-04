from django.db import models
from django.utils.text import slugify
# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=200)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    heading = models.CharField(max_length=200)
    preview = models.CharField(max_length=555)
    imgg = models.FileField(upload_to='blog',null=True,blank=True)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.heading)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.heading    