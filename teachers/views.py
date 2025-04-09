# teachers/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Teacher
from .serializers import TeacherSerializer
from .forms import TeacherProfileForm
from students.models import Course


# Kiểm tra xem user có phải là superuser (giáo viên)
def is_superuser(user):
    return user.is_superuser

# ViewSet cho API
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Chỉ superuser mới truy cập được API

    def perform_create(self, serializer):
        # Gán user hiện tại cho teacher khi tạo mới qua API
        serializer.save(user=self.request.user)

# View thông thường cho giao diện web
@login_required
@user_passes_test(is_superuser)
def teacher_profile(request):
    user = request.user
    try:
        teacher = Teacher.objects.get(user=user)
        # Lấy danh sách các khóa học mà teacher phụ trách
        enrolled_courses = Course.objects.filter(instructor=teacher)
        return render(request, 'teachers/teacher_profile.html', {
            'teacher': teacher,
            'enrolled_courses': enrolled_courses,
            'is_superuser': user.is_superuser
        })
    except Teacher.DoesNotExist:
        if request.method == 'POST':
            form = TeacherProfileForm(request.POST, request.FILES)
            if form.is_valid():
                teacher = form.save(commit=False)
                teacher.user = user
                teacher.save()
                messages.success(request, 'Hồ sơ giáo viên đã được tạo thành công!')
                return redirect('teachers:teacher_profile')
        else:
            form = TeacherProfileForm()
        return render(request, 'teachers/teacher_profile_create.html', {
            'form': form,
            'is_superuser': user.is_superuser
        })

@login_required
@user_passes_test(is_superuser)
def teacher_profile_edit(request):
    user = request.user
    try:
        teacher = Teacher.objects.get(user=user)
    except Teacher.DoesNotExist:
        messages.error(request, 'Bạn chưa có hồ sơ giáo viên để chỉnh sửa.')
        return redirect('teachers:teacher_profile')

    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hồ sơ giáo viên đã được cập nhật thành công!')
            return redirect('teachers:teacher_profile')
    else:
        form = TeacherProfileForm(instance=teacher)
    
    return render(request, 'teachers/teacher_profile_edit.html', {
        'form': form,
        'teacher': teacher,
        'is_superuser': user.is_superuser
    })