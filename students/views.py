from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from .models import Student, Course, Enrollment, Attendance, Document, Forum, Comment
from .serializers import (
    StudentSerializer, CourseSerializer, EnrollmentSerializer,
    AttendanceSerializer, DocumentSerializer, ForumSerializer, CommentSerializer
)
from teachers.models import Teacher

# API đăng nhập
@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'is_superuser': user.is_superuser
        })
    return Response({'error': 'Tên đăng nhập hoặc mật khẩu không đúng'}, status=400)

# API đăng ký
@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        if not all([username, email, password]):
            return Response({'error': 'Thiếu thông tin bắt buộc'}, status=400)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'is_superuser': user.is_superuser
        })
    except Exception as e:
        return Response({'error': str(e)}, status=400)

# API ViewSets
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            user = User.objects.create_user(
                username=data['email'],
                email=data['email'],
                password='defaultpassword'  # Có thể yêu cầu password từ client
            )
            student_data = {**data, 'user': user.id}
            serializer = self.get_serializer(data=student_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'error': str(e)}, status=400)
        except Exception as e:
            return Response({'error': 'Không thể tạo học viên'}, status=400)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            course_data = {**data}
            if not course_data.get('instructor'):
                default_teacher = Teacher.objects.first()
                course_data['instructor'] = default_teacher.id if default_teacher else None
            serializer = self.get_serializer(data=course_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'error': str(e)}, status=400)
        except Exception as e:
            return Response({'error': 'Không thể tạo khóa học'}, status=400)

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            try:
                student = Student.objects.get(user=request.user)
            except Student.DoesNotExist:
                return Response({'error': 'Học viên không tồn tại'}, status=400)
            course = Course.objects.get(id=data['course'])
            if float(data.get('fee_paid', 0)) < course.fee:
                return Response({'error': 'Số tiền thanh toán không đủ'}, status=400)
            enrollment_data = {**data, 'student': student.id}
            serializer = self.get_serializer(data=enrollment_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data)
        except Course.DoesNotExist:
            return Response({'error': 'Khóa học không tồn tại'}, status=400)
        except ValidationError as e:
            return Response({'error': str(e)}, status=400)
        except Exception as e:
            return Response({'error': 'Không thể đăng ký khóa học'}, status=400)

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'error': str(e)}, status=400)
        except Exception as e:
            return Response({'error': 'Không thể tạo điểm danh'}, status=400)

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            document_data = {**data, 'uploaded_by': request.user.id}
            serializer = self.get_serializer(data=document_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'error': str(e)}, status=400)
        except Exception as e:
            return Response({'error': 'Không thể tải lên tài liệu'}, status=400)

class ForumViewSet(viewsets.ModelViewSet):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            forum_data = {**data, 'created_by': request.user.id}
            serializer = self.get_serializer(data=forum_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'error': str(e)}, status=400)
        except Exception as e:
            return Response({'error': 'Không thể tạo diễn đàn'}, status=400)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            comment_data = {**data, 'user': request.user.id}
            serializer = self.get_serializer(data=comment_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'error': str(e)}, status=400)
        except Exception as e:
            return Response({'error': 'Không thể tạo bình luận'}, status=400)

# API-specific views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_forum(request, pk):
    try:
        forum = Forum.objects.get(pk=pk)
        if request.user in forum.likes.all():
            forum.likes.remove(request.user)
            liked = False
        else:
            forum.likes.add(request.user)
            liked = True
        return Response({'like_count': forum.likes.count(), 'liked': liked})
    except Forum.DoesNotExist:
        return Response({'error': 'Diễn đàn không tồn tại'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_comment(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            liked = False
        else:
            comment.likes.add(request.user)
            liked = True
        return Response({'like_count': comment.likes.count(), 'liked': liked})
    except Comment.DoesNotExist:
        return Response({'error': 'Bình luận không tồn tại'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, forum_id):
    try:
        forum = Forum.objects.get(pk=forum_id)
        data = request.data
        comment_data = {
            'forum': forum.id,
            'user': request.user.id,
            'content': data.get('content'),
            'parent': data.get('parent'),
            'image': data.get('image'),
            'file': data.get('file')
        }
        serializer = CommentSerializer(data=comment_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    except Forum.DoesNotExist:
        return Response({'error': 'Diễn đàn không tồn tại'}, status=404)

# API báo cáo
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_report_api(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_report_api(request):
    courses = Course.objects.annotate(num_students=Count('enrollment'))
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attendance_report_api(request):
    attendance_stats = Attendance.objects.values('course__name').annotate(
        num_attended=Count('status', filter=Q(status='Present')),
        num_missed=Count('status', filter=Q(status='Absent'))
    )
    return Response(attendance_stats)