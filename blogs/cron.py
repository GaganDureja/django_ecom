
from . models import *
import random

def add_cat():
    number = random.randint(0,100)
    Category.objects.create(name=number)