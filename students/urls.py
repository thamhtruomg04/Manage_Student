# student_management/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import path, include
from .views import (
    create_comment, like_comment, like_forum, student_list, student_create, student_edit, student_delete,
    course_list, course_create, course_edit, course_delete, course_register, enrollment_list, register,
    login_view, logout_view, home, student_profile, attendance_list, take_attendance, attendance_edit,
    attendance_delete, document_list, document_create, document_delete, student_report, course_report,
    attendance_report, reporters, forum_list, forum_detail, forum_create, forum_edit, forum_delete,
    comment_edit, comment_delete, profile, 
)
from rest_framework.routers import DefaultRouter
from .api_views import StudentViewSet, CourseViewSet, EnrollmentViewSet, AttendanceViewSet, DocumentViewSet, ForumViewSet, CommentViewSet

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
    path('api/', include(router.urls)),

    # Student-related URLs
    path('', student_list, name='student_list'),
    path('new/', student_create, name='student_create'),
    path('<int:pk>/edit/', student_edit, name='student_edit'),
    path('<int:pk>/delete/', student_delete, name='student_delete'),
    path('students/<int:pk>/', student_profile, name='student_profile'),
    path('reports/students/', student_report, name='student_report'),

    # Course-related URLs
    path('courses/', course_list, name='course_list'),
    path('courses/new/', course_create, name='course_create'),
    path('courses/<int:pk>/edit/', course_edit, name='course_edit'),
    path('courses/<int:pk>/delete/', course_delete, name='course_delete'),
    path('courses/<int:pk>/register/', course_register, name='course_register'),
    path('courses/<int:pk>/enrollments/', enrollment_list, name='enrollment_list'),
    path('reports/courses/', course_report, name='course_report'),

    # Authentication URLs
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home, name='home'),

    # Attendance-related URLs
    path('attendance/', attendance_list, name='attendance_list'),
    path('take-attendance/', take_attendance, name='take_attendance'),
    path('attendance/<int:pk>/', attendance_edit, name='attendance_edit'),
    path('attendance/<int:pk>/delete/', attendance_delete, name='attendance_delete'),
    path('reports/attendance/', attendance_report, name='attendance_report'),

    # Document-related URLs
    path('documents/', document_list, name='document_list'),
    path('documents/upload/', document_create, name='document_create'),
    path('documents/delete/<int:pk>/', document_delete, name='document_delete'),

    # Forum-related URLs
    path('forums/', forum_list, name='forum_list'),
    path('forums/<int:pk>/', forum_detail, name='forum_detail'),
    path('forums/create/', forum_create, name='forum_create'),
    path('forums/<int:pk>/edit/', forum_edit, name='forum_edit'),
    path('forums/<int:pk>/delete/', forum_delete, name='forum_delete'),
    path('forum/<int:pk>/like/', like_forum, name='like_forum'),  # Thêm endpoint cho like_forum
    path('forum/<int:forum_id>/comment/', create_comment, name='create_comment'),  # Endpoint cho tạo bình luận/phản hồi

    # Comment-related URLs
    path('comments/<int:pk>/edit/', comment_edit, name='comment_edit'),  # Sửa lỗi cú pháp (thêm dấu / trước edit)
    path('comments/<int:pk>/delete/', comment_delete, name='comment_delete'),
    path('comment/<int:pk>/like/', like_comment, name='like_comment'),  # Sửa comment_id thành pk cho đồng bộ

    # Report-related URLs
    path('reports/', reporters, name='reporters'),

    # Media serving
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),

    path('profile/', profile, name='profile'),  # Thêm đường dẫn đến trang cá nhân
    
]

# Thêm static và media URLs khi ở chế độ DEBUG
if settings.DEBUG:
    print("Serving media at:", settings.MEDIA_URL, "from:", settings.MEDIA_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)