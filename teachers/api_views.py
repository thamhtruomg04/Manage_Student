# teachers/api_views.py
from rest_framework import viewsets
from students.models import Course
from teachers.models import Teacher
from serializers import TeacherSerializer

class TeacherProfileViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get_queryset(self):
        # Sửa từ instructor_name thành instructor
        return Course.objects.filter(instructor=self.request.user.teacher_profile)