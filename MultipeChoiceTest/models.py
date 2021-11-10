from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subjects = models.ManyToManyField('Subject', blank=True, verbose_name="Môn thi")

    def __str__(self):
        return self.user.username

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subjects = models.ManyToManyField('Subject', blank=True, verbose_name="Môn thi")

    def __str__(self):
        return self.user.username

class ExamAbstract(models.Model):
    title = models.TextField()

    class Meta:
        abstract = True

class Subject(ExamAbstract):
    
    def __str__(self):
        return self.title

class Question(ExamAbstract):
    exam_c = models.ForeignKey("Exam", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Choice(ExamAbstract):
    question_c = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.title
  

class Exam(ExamAbstract):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now=True)
    duration = models.IntegerField(verbose_name="Thời gian làm bài thi", help_text="Tính bằng phút")
    STATUS_CHOICES = [
        ('wait', 'Chưa mở'),
        ('open', 'Đang mở'),
        ('close', 'Đã đóng'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='wait')

    def __str__(self):
        return '%s - %s - %s' % (self.title, self.subject, self.teacher)


class StudentExam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    joined = models.DateTimeField(auto_now_add=True)
    is_finish = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['student', 'exam']
        

class StudentExamQuestion(models.Model):
    student_exam = models.ForeignKey(StudentExam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)