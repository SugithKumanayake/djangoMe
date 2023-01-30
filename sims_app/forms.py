from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from .models import *

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CreateStudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'sid': forms.TextInput(attrs={'class': 'form-control'}),
            'fname': forms.TextInput(attrs={'class': 'form-control'}),
            'lname': forms.TextInput(attrs={'class': 'form-control'}),
            'bdate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'yyyy-mm-dd'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'other_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control','placeholder': 'someone@xyz.com'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            }

class CreateStudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'quali_type': forms.Select(attrs={'class': 'form-control'}),
            'quali_detail': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CreateCourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'cid': forms.TextInput(attrs={'class': 'form-control'}),
            'cname': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'ctype': forms.Select(attrs={'class': 'form-control'}),
            'fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'medium': forms.Select(attrs={'class': 'form-control'}),
            }

class CreateEnrollForm(ModelForm):
    class Meta:
        model = Enroll
        fields = '__all__'
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'yyyy-mm-dd'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'yyyy-mm-dd'}),
            }

class CreatePaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'pay_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'yyyy-mm-dd'}),
            'pay_type': forms.Select(attrs={'class': 'form-control'}),
            'pay_note': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            }

class CreateExamForm(ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'exam_id': forms.TextInput(attrs={'class': 'form-control'}),
            'module': forms.TextInput(attrs={'class': 'form-control'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'grade': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.TextInput(attrs={'class': 'form-control'}),

        }