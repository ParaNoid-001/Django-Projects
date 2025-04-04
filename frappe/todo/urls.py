from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('new/', views.task_create, name='task_create'),
    path('tasks/', views.get_tasks, name='get_tasks'),
    path('done/<int:task_id>/', views.mark_task_done, name='mark_task_done'),
    path('edit/<int:task_id>/', views.edit_task_page, name='edit_task_page'),
    path('delete/<int:task_id>/', views.task_delete, name='task_delete'),
    path('update/<int:task_id>/', views.task_edit, name='task_edit'),
    path('show_tasks/', views.show_tasks, name='show_tasks'),
]

