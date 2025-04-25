from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentViewSet, CourseViewSet, EnrollmentViewSet, AttendanceViewSet,
    DocumentViewSet, ForumViewSet, CommentViewSet, login_api, register_api,
    like_forum, like_comment, create_comment, student_report_api,
    course_report_api, attendance_report_api
)

app_name = 'students'

# Định nghĩa router cho API
router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'forums', ForumViewSet)
router.register(r'comments', CommentViewSet)

# Định nghĩa các URL patterns
urlpatterns = [
    # API endpoints
    path('v1/', include(router.urls)),
    path('v1/login/', login_api, name='login_api'),
    path('v1/register/', register_api, name='register_api'),
    path('v1/forum/<int:pk>/like/', like_forum, name='like_forum'),
    path('v1/forum/<int:forum_id>/comment/', create_comment, name='create_comment'),
    path('v1/comment/<int:pk>/like/', like_comment, name='like_comment'),
    path('v1/reports/students/', student_report_api, name='student_report_api'),
    path('v1/reports/courses/', course_report_api, name='course_report_api'),
    path('v1/reports/attendance/', attendance_report_api, name='attendance_report_api'),
]