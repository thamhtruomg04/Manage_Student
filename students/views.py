# student_management/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Q
from .models import Student, Course, Enrollment, Attendance, Document, Forum, Comment
from .forms import StudentForm, CourseForm, UserRegisterForm, AttendanceForm, DocumentForm, ForumForm, CommentForm

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
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password='defaultpassword'
            )
            student = form.save(commit=False)
            student.user = user
            student.save()
            messages.success(request, 'Học viên đã được tạo thành công!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Học viên đã được cập nhật thành công!')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form, 'edit': True})

@login_required
@user_passes_test(is_superuser)
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Học viên đã được xóa thành công!')
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})

# Course list view
@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'students/course_list.html', {'courses': courses})

@login_required
@user_passes_test(is_superuser)
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            student_id = request.POST.get('student')
            if student_id:
                student = Student.objects.get(pk=student_id)
                Enrollment.objects.create(student=student, course=course)
            messages.success(request, 'Khóa học đã được tạo thành công!')
            return redirect('course_list')
    else:
        form = CourseForm()
    students = Student.objects.all()
    return render(request, 'students/course_form.html', {'form': form, 'students': students})

@login_required
@user_passes_test(is_superuser)
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            student_id = request.POST.get('student')
            if student_id:
                student = Student.objects.get(pk=student_id)
                enrollment, created = Enrollment.objects.get_or_create(student=student, course=course)
            messages.success(request, 'Khóa học đã được cập nhật thành công!')
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    students = Student.objects.all()
    return render(request, 'students/course_form.html', {'form': form, 'students': students, 'edit': True})

@login_required
@user_passes_test(is_superuser)
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Khóa học đã được xóa thành công!')
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
            student=user.username,
            email=user.email,
        )

    if request.method == 'POST':
        payment_amount = request.POST.get('payment_amount')
        if payment_amount and float(payment_amount) >= course.fee:
            enrollment, created = Enrollment.objects.get_or_create(student=student, course=course)
            if created:
                enrollment.fee_paid = float(payment_amount)
                enrollment.save()
                messages.success(request, 'Đăng ký thành công!')
            else:
                messages.info(request, 'Bạn đã đăng ký khóa học này rồi.')
            return redirect('course_list')
        else:
            messages.error(request, 'Thanh toán không thành công. Vui lòng kiểm tra lại số tiền.')
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
            messages.success(request, 'Điểm danh đã được cập nhật thành công!')
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
        messages.success(request, 'Điểm danh đã được xóa thành công!')
        return redirect('attendance_list')
    return render(request, 'students/attendance_confirm_delete.html', {'attendance': attendance})

@login_required
def document_list(request):
    documents = Document.objects.all()
    return render(request, 'students/document_list.html', {'documents': documents})

@login_required
@user_passes_test(is_superuser)
def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()
            messages.success(request, 'Tài liệu đã được tải lên thành công!')
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'students/document_form.html', {'form': form})

@login_required
def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Tài liệu đã được xóa thành công!')
        return redirect('document_list')
    return render(request, 'students/document_confirm_delete.html', {'document': document})

@login_required
def student_report(request):
    students = Student.objects.all()
    return render(request, 'students/student_report.html', {'students': students})

@login_required
def course_report(request):
    courses = Course.objects.annotate(num_students=Count('enrollment'))
    return render(request, 'students/course_report.html', {'courses': courses})

@login_required
def attendance_report(request):
    attendance_stats = Attendance.objects.values('course__name').annotate(
        num_attended=Count('status', filter=Q(status=True)),
        num_missed=Count('status', filter=Q(status=False))
    )
    return render(request, 'students/attendance_report.html', {'attendance_stats': attendance_stats})

@login_required
def reporters(request):
    return render(request, 'students/reports.html')

# Forum-related views
@login_required
def forum_list(request):
    forums = Forum.objects.all()
    return render(request, 'students/forum_list.html', {'forums': forums})

@login_required
def forum_detail(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    comments = forum.comments.filter(parent=None)
    return render(request, 'students/forum_detail.html', {'forum': forum, 'comments': comments})

@login_required
@user_passes_test(is_superuser)
def forum_create(request):
    if request.method == 'POST':
        form = ForumForm(request.POST, request.FILES)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.created_by = request.user
            forum.save()
            messages.success(request, 'Diễn đàn đã được tạo thành công!')
            return redirect('forum_list')
    else:
        form = ForumForm()
    return render(request, 'students/forum_form.html', {'form': form})

@login_required
def forum_edit(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    if request.user != forum.created_by and not request.user.is_superuser:
        messages.error(request, 'Bạn không có quyền chỉnh sửa diễn đàn này.')
        return redirect('forum_list')
    if request.method == 'POST':
        form = ForumForm(request.POST, request.FILES, instance=forum)
        if form.is_valid():
            form.save()
            messages.success(request, 'Diễn đàn đã được cập nhật thành công!')
            return redirect('forum_list')
    else:
        form = ForumForm(instance=forum)
    return render(request, 'students/forum_form.html', {'form': form, 'edit': True})

@login_required
def forum_delete(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    if request.user != forum.created_by and not request.user.is_superuser:
        messages.error(request, 'Bạn không có quyền xóa diễn đàn này.')
        return redirect('forum_list')
    if request.method == 'POST':
        forum.delete()
        messages.success(request, 'Diễn đàn đã được xóa thành công!')
        return redirect('forum_list')
    return render(request, 'students/forum_confirm_delete.html', {'forum': forum})
@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.user and not request.user.is_superuser:
        messages.error(request, 'Bạn không có quyền chỉnh sửa bình luận này.')
        return redirect('forum_detail', pk=comment.forum.pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bình luận đã được cập nhật thành công!')
            return redirect('forum_detail', pk=comment.forum.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'students/comment_form.html', {'form': form})

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.user and not request.user.is_superuser:
        messages.error(request, 'Bạn không có quyền xóa bình luận này.')
        return redirect('forum_detail', pk=comment.forum.pk)
    if request.method == 'POST':
        forum_pk = comment.forum.pk
        comment.delete()
        messages.success(request, 'Bình luận đã được xóa thành công!')
        return redirect('forum_detail', pk=forum_pk)
    return render(request, 'students/comment_confirm_delete.html', {'comment': comment})

@login_required
def like_forum(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    if request.method != 'POST':
        return JsonResponse({'error': 'Phương thức không được hỗ trợ'}, status=405)
    if request.user in forum.likes.all():
        forum.likes.remove(request.user)
        liked = False
    else:
        forum.likes.add(request.user)
        liked = True
    return JsonResponse({'like_count': forum.likes.count(), 'liked': liked})

@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method != 'POST':
        return JsonResponse({'error': 'Phương thức không được hỗ trợ'}, status=405)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True
    return JsonResponse({'like_count': comment.likes.count(), 'liked': liked})

@login_required
def create_comment(request, forum_id):
    if request.method == "POST":
        forum = get_object_or_404(Forum, pk=forum_id)
        content = request.POST.get("content")
        parent_id = request.POST.get("parent")
        image = request.FILES.get("image")
        file = request.FILES.get("file")

        if not content:
            return JsonResponse({"error": "Nội dung không được để trống"}, status=400)

        comment = Comment.objects.create(
            forum=forum,
            user=request.user,
            content=content,
            parent_id=parent_id,
            image=image,
            file=file
        )

        return JsonResponse({
            "id": comment.id,
            "username": comment.user.username,
            "content": comment.content,
            "created_at": comment.created_at.isoformat(),
            "image": comment.image.url if comment.image else None,
            "file": comment.file.url if comment.file else None,
            "user_is_owner": comment.user == request.user
        })
    return JsonResponse({"error": "Phương thức không được hỗ trợ"}, status=405)