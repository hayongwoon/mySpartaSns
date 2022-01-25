from django.contrib import admin
from .models import MyPizza, MyTopping

# Register your models here.

admin.site.register(MyTopping)
admin.site.register(MyPizza)
