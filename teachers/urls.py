from django.urls import path
from .views import (
    TeacherListCreateAPIView, TeacherRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('', TeacherListCreateAPIView.as_view(), name='teacher_list_create'),
    path('<int:pk>/', TeacherRetrieveUpdateDestroyAPIView.as_view(), name='teacher_retrieve_update_destroy'),
]