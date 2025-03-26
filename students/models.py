from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    class_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.student

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.teacher_name
    
    

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    credits = models.IntegerField()
    instructor_name = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    fee_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.student} - {self.course}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Có mặt'), ('Absent', 'Vắng mặt')], null=True, blank=True)
    participation = models.CharField(
        max_length=20,
        choices=[('Active', 'Học tích cực'), ('Inactive', 'Không tích cực')],
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.student} - {self.course} - {self.date} - {self.status or 'No status'} - {self.participation or 'No participation'}"

class Document(models.Model):
    title = models.CharField(max_length=255)
    upload = models.FileField(upload_to='documents/')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Forum(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='forum_images/', null=True, blank=True)  # Thêm ảnh
    file = models.FileField(upload_to='forum_files/', null=True, blank=True)  # Thêm file
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    image = models.ImageField(upload_to='comment_images/', null=True, blank=True)
    file = models.FileField(upload_to='comment_files/', null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.forum.title}"
