from django import forms
from django.db.models import fields
from django.forms import ModelForm, widgets
import datetime

from .models import *
from django.contrib.auth.models import User

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'
    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)


class ExamForm(ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'
        widgets = {
        'teacher': forms.HiddenInput(),
        'subject': forms.HiddenInput(),
        'title': forms.TextInput(attrs={
            'class': 'form-control'
        }),
        'duration': forms.NumberInput(attrs={
            'class': 'form-control'
        }),
        'status': forms.Select(attrs={
            'class': 'form-select'
        }),

        }
        labels = {
            'title': "Tên môn thi"
        }


class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['password','first_name', 'last_name', 'email']
        widgets = {
            'password': forms.TextInput(
                attrs={
                    'class': 'form-control mb-2'
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control mb-2'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control mb-2'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control mb-2'
                }
            )
        }

class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput(),
            'subjects': forms.SelectMultiple(
                attrs={
                'class': 'form-select'

                }

            )
        }
class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput(),
            'subjects': forms.SelectMultiple(
                attrs={
                'class': 'form-select'

                }

            )
        }

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        widgets = {
            'exam_c': forms.HiddenInput(),
        }