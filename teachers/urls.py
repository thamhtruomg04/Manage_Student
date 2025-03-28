# teachers/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'teachers', views.TeacherViewSet)

app_name = 'teachers'

urlpatterns = [
    # URL cho giao diện web
    path('profile/', views.teacher_profile, name='teacher_profile'),
    path('profile/edit/', views.teacher_profile_edit, name='teacher_profile_edit'),
    # URL cho API
    path('api/', include(router.urls)),
]