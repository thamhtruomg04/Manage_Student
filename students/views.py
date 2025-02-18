from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Course, Enrollment, Attendance
from .forms import StudentForm, CourseForm, UserRegisterForm, AttendanceForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

# Check if the user is a superuser
def is_superuser(user):
    return user.is_superuser

# Register view
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Tài khoản cho {username} đã được tạo!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'students/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng')
    return render(request, 'students/login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# Home view
@login_required
def home(request):
    return render(request, 'students/home.html')

# Student list view
@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

@login_required
@user_passes_test(is_superuser)
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)  # Thêm request.FILES
        if form.is_valid():
            # Tạo đối tượng User trước khi tạo đối tượng Student
            user = User.objects.create_user(
                username=form.cleaned_data['email'],  # Sử dụng email làm username
                email=form.cleaned_data['email'],
                password='defaultpassword'  # Bạn có thể đặt một mật khẩu mặc định hoặc tạo một mật khẩu ngẫu nhiên
            )
            student = form.save(commit=False)
            student.user = user
            student.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)  # Thêm request.FILES
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form, 'edit': True})

# Student delete view (only for superusers)
@login_required
@user_passes_test(is_superuser)
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})

# Course list view
@login_required
def course_list(request):
    enrollments = Enrollment.objects.select_related('student', 'course').all()
    return render(request, 'students/course_list.html', {'enrollments': enrollments})

# Course create view (only for superusers)
@login_required
@user_passes_test(is_superuser)
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            # Liên kết học viên với khóa học mới tạo
            student_id = request.POST.get('student')
            if student_id:
                student = Student.objects.get(pk=student_id)
                Enrollment.objects.create(student=student, course=course)
            return redirect('course_list')
    else:
        form = CourseForm()
    students = Student.objects.all()  # Lấy danh sách học viên
    return render(request, 'students/course_form.html', {'form': form, 'students': students})

# Course edit view (only for superusers)
@login_required
@user_passes_test(is_superuser)
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            # Cập nhật liên kết học viên với khóa học
            student_id = request.POST.get('student')
            if student_id:
                student = Student.objects.get(pk=student_id)
                enrollment, created = Enrollment.objects.get_or_create(student=student, course=course)
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    students = Student.objects.all()  # Lấy danh sách học viên
    return render(request, 'students/course_form.html', {'form': form, 'students': students, 'edit': True})

# Course delete view (only for superusers)
@login_required
@user_passes_test(is_superuser)
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'students/course_confirm_delete.html', {'course': course})

# Course registration view
@login_required
def course_register(request, pk):
    course = get_object_or_404(Course, pk=pk)
    user = request.user
    try:
        student = Student.objects.get(user=user)
    except Student.DoesNotExist:
        student = Student.objects.create(
            user=user,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )

    if request.method == 'POST':
        enrollment, created = Enrollment.objects.get_or_create(student=student, course=course)
        if created:
            messages.success(request, 'Đăng ký thành công!')
        else:
            messages.info(request, 'Bạn đã đăng ký khóa học này rồi.')
        return redirect('course_list')

    return render(request, 'students/course_register.html', {'course': course, 'username': user.username})

# Enrollment list view
@login_required
def enrollment_list(request, pk):
    course = get_object_or_404(Course, pk=pk)
    enrollments = Enrollment.objects.filter(course=course)
    return render(request, 'students/enrollment_list.html', {'course': course, 'enrollments': enrollments})

@login_required
def student_profile(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_profile.html', {'student': student})


@login_required
def attendance_list(request):
    attendances = Attendance.objects.all()
    return render(request, 'students/attendance_list.html', {'attendances': attendances})

@login_required
@user_passes_test(is_superuser)
def take_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Điểm danh thành công!')
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'students/take_attendance.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def attendance_edit(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm(instance=attendance)
    return render(request, 'students/take_attendance.html', {'form': form, 'edit': True})

@login_required
@user_passes_test(is_superuser)
def attendance_delete(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        attendance.delete()
        return redirect('attendance_list')
    return render(request, 'students/attendance_confirm_delete.html', {'attendance': attendance})
