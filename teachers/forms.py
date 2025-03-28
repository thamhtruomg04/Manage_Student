# teachers/forms.py
from django import forms
from .models import Teacher

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['teacher_name', 'date_of_birth', 'email', 'phone_number', 'avatar', 'department', 'hire_date']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        }