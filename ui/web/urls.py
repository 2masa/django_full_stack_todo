from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home', views.home, name='home'),
    path('todos', views.get_todos, name='get_todos'),
    path('todo/add', views.add_todo, name='add_todo'),
    path('todo/edit/<uuid:todo_id>', views.edit_todo, name='edit_todo'),
    path('todo/delete/<uuid:todo_id>', views.delete_todo, name='delete_todo'),
]