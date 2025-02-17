from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import student_list, student_create, student_edit, student_delete, course_list, course_create, course_edit, course_delete, course_register, enrollment_list, register, login_view, logout_view, home, student_profile

urlpatterns = [
    path('', student_list, name='student_list'),
    path('new/', student_create, name='student_create'),
    path('<int:pk>/edit/', student_edit, name='student_edit'),
    path('<int:pk>/delete/', student_delete, name='student_delete'),
    path('courses/', course_list, name='course_list'),
    path('courses/new/', course_create, name='course_create'),
    path('courses/<int:pk>/edit/', course_edit, name='course_edit'),
    path('courses/<int:pk>/delete/', course_delete, name='course_delete'),
    path('courses/<int:pk>/register/', course_register, name='course_register'),
    path('courses/<int:pk>/enrollments/', enrollment_list, name='enrollment_list'),
    path('students/<int:pk>/', student_profile, name='student_profile'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
