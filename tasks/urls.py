from django.urls import path
from .views import TaskListCreateView, TaskDetailView

urlpatterns = [
    path(
        'tasks/',
        TaskListCreateView.as_view()
    ),
    path(
        'task/<int:pk>/',
        TaskDetailView.as_view()
    ),
]