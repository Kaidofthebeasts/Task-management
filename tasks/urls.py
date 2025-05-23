# tasks/urls.py
from django.urls import path
from .views import (
    HomeView,
    TaskListView, TaskCreateView, TaskDetailView, TaskUpdateView, TaskDeleteView,
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, DashboardView, NotificationListView
)
urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('list/', TaskListView.as_view(), name='task_list'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'), 
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'), 
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'), 
    
    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    
    #Dashboard URL
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
     #Notification URLs
    path('notifications/', NotificationListView.as_view(), name='notification_list'),

]
