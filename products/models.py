from django.db import models
from django.utils.text import slugify
# Create your models here.


class category(models.Model):    
    name = models.CharField(max_length=200)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(category, self).save(*args, **kwargs)

    

    def __str__(self):
        return self.name

class sub_category(models.Model):
    category = models.ForeignKey(category,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    slug = models.SlugField(unique=True, blank=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(sub_category, self).save(*args, **kwargs)


    def __str__(self):
        return self.name


class brand(models.Model):
    name = models.CharField(max_length=100)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class product(models.Model):
    category = models.ForeignKey(category,on_delete=models.CASCADE)
    sub_category = models.ForeignKey(sub_category,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(brand,on_delete=models.CASCADE)
    mrp = models.IntegerField()
    price = models.IntegerField()
    imgg = models.FileField(upload_to='product',null=True,blank=True)
    description = models.TextField()
    stock = models.IntegerField()    
    sort_no = models.IntegerField() 
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Banner(models.Model):    
    imgg = models.FileField(upload_to='banner',null=True,blank=True)
    heading = models.CharField(max_length=255)
    description = models.CharField(max_length=555)
    category = models.ForeignKey(category,on_delete=models.SET_DEFAULT,default=None,null=True,blank=True)
    sub_category = models.ForeignKey(sub_category,on_delete=models.SET_DEFAULT,default=None,null=True,blank=True)
    product = models.ForeignKey(product,on_delete=models.SET_DEFAULT,default=None,null=True,blank=True)
    sort_no = models.IntegerField() 
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading
    

class Rating(models.Model):
    pass


    