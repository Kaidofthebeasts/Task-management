# tasks/admin.py
from django.contrib import admin
from .models import Task, Category, Notification

# Register your models here.
admin.site.register(Category) 
admin.site.register(Task)  
admin.site.register(Notification)   
