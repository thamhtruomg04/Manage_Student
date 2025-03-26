from django import forms
from .models import Student, Course, Attendance, Document, Forum, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student', 'date_of_birth', 'email', 'phone_number', 'address', 'avatar']

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'start_date', 'end_date', 'credits', 'instructor_name', 'fee']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'course', 'date', 'status', 'participation']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'upload', 'course']

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['title', 'description', 'image', 'file', 'course']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['forum', 'content', 'parent', 'image', 'file', 'likes', 'user']  # Loại bỏ 'created_at' và 'updated_at'
        widgets = {
            'parent': forms.HiddenInput()  # Giữ parent ở dạng ẩn
        }

