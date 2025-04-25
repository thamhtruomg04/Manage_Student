from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student, Course, Enrollment, Attendance, Document, Forum, Comment
from teachers.models import Teacher

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_superuser']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'student', 'date_of_birth', 'email', 'phone_number', 'address', 'avatar', 'class_name']

    def validate_email(self, value):
        if Student.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email đã tồn tại")
        return value

class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), allow_null=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'credits', 'instructor', 'fee']

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("Ngày bắt đầu phải trước ngày kết thúc")
        return data

class EnrollmentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), source='student', write_only=True)
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), source='course', write_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'student_id', 'course_id', 'enrollment_date', 'fee_paid']

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'course', 'date', 'status', 'participation']

    def validate(self, data):
        if Attendance.objects.filter(student=data['student'], course=data['course'], date=data['date']).exists():
            raise serializers.ValidationError("Điểm danh cho học viên này trong ngày này đã tồn tại")
        return data

class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    uploaded_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='uploaded_by', write_only=True)

    class Meta:
        model = Document
        fields = ['id', 'title', 'upload', 'course', 'uploaded_by', 'uploaded_by_id', 'upload_date']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'forum', 'user', 'user_id', 'content', 'created_at', 'updated_at', 'parent', 'image', 'file', 'likes']

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Nội dung không được để trống")
        return value

class ForumSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='created_by', write_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Forum
        fields = ['id', 'title', 'description', 'image', 'file', 'course', 'created_by', 'created_by_id', 'created_at', 'comments']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Tiêu đề không được để trống")
        return value