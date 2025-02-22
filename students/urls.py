# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import student_list, student_create, student_edit, student_delete, course_list, course_create, course_edit, course_delete, course_register, enrollment_list, register, login_view, logout_view, home, student_profile, attendance_list, take_attendance, attendance_edit, attendance_delete , document_list, document_create, document_delete, student_report, course_report, attendance_report, reporters, forum_list, forum_detail, forum_create, forum_edit, forum_delete

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
    path('attendance/', attendance_list, name='attendance_list'),
    path('take-attendance/', take_attendance, name='take_attendance'),
    path('attendance/<int:pk>/', attendance_edit, name='attendance_edit'),
    path('attendance/<int:pk>/delete/', attendance_delete, name='attendance_delete'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home, name='home'),
    path('documents/', document_list, name='document_list'),
    path('documents/upload/', document_create, name='document_create'),
    path('documents/delete/<int:pk>/', document_delete, name='document_delete'),
    path('reports/students/', student_report, name='student_report'),
    path('reports/courses/', course_report, name='course_report'),
    path('reports/attendance/', attendance_report, name='attendance_report'),
    path('reports/', reporters, name='reporters'),
    path('forums/', forum_list, name='forum_list'),
    path('forums/<int:pk>/', forum_detail, name='forum_detail'),
    path('forums/create/', forum_create, name='forum_create'),
    path('forums/<int:pk>/edit/', forum_edit, name='forum_edit'),
    path('forums/<int:pk>/delete/', forum_delete, name='forum_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
