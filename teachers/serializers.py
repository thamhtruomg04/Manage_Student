# teachers/serializers.py
from rest_framework import serializers
from .models import Teacher

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'user', 'teacher_name', 'date_of_birth', 'email', 'phone_number', 'avatar', 'department', 'hire_date']
        read_only_fields = ['user']  # User sẽ được gán tự động, không cho chỉnh sửa qua API