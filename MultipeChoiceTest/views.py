from django.contrib.auth import login, logout
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

from django.contrib import messages

import datetime
from django.utils import timezone

# Create your views here.

@login_required
def index(request):
    login_user = request.user

    teacher = Teacher.objects.filter(user=login_user)
    student = Student.objects.filter(user=login_user)
    if teacher:
        subjects = Subject.objects.filter(
            teacher__user=request.user
        )
    elif student:
        subjects = Subject.objects.filter(
            student__user=request.user
        )
    else:
        return Http404

    context = {
        'subjects': subjects
    }
    return render(request, 'index.html', context)


@login_required
def subject(request, id):
    context = {

    }
    try:
        subject = Subject.objects.get(
            pk=id,
            teacher__user=request.user
            )
        exams = Exam.objects.filter(subject=id, teacher=request.user.teacher )
            
        if request.method == "POST":
            form = ExamForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, request.POST['title'])
                return redirect('subject', id=id)
        else:
            form = ExamForm(initial=
            {
                'subject': subject.id,
                'teacher': request.user.teacher,
                'status': 'wait'
            })

        context['form'] = form

    except:
        subject = Subject.objects.get(
            pk=id,
            student__user=request.user
            )
        exams = Exam.objects.filter(subject=id)

    


    context['subject'] = subject
    context['exams'] = exams



    return render(request, 'subject.html', context)


@login_required
def profile(request):
    if request.method == "POST" and "updateUserBtn" in request.POST:
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhập hồ sơ người dùng thành công')
            return redirect('profile')
    else:
        user_form = UserProfileForm(instance=request.user)

    
    if request.method == "POST" and 'updateSubjectBtn' in request.POST:
        
        try:
            login_user = request.user.teacher
            form = TeacherForm(request.POST, instance=login_user)

        except:
            login_user = request.user.student
            form = StudentForm(request.POST, instance=login_user)

        if form.is_valid:
            form.save()
            
            messages.success(request, 'Cập nhập môn thi thành công')

            return redirect('profile')
    else:
        try:
            subject_form = TeacherForm(instance=request.user.teacher)
            exams = Exam.objects.filter(
                teacher=request.user.teacher
            )
        except:
            subject_form = TeacherForm(instance=request.user.student)
            exams = Exam.objects.filter(
                studentexam__student = request.user.student
            )



    context = {

        'user_form': user_form,
        'teacher_form': subject_form,
        'exams': exams

    }

    return render(request, 'registration/profile.html', context)

@login_required
def exam(request, id):
    lgin_user = request.user
    if Teacher.objects.filter(user=lgin_user):
        is_teacher = True
    else:
        is_teacher = False
    
    exam = Exam.objects.get(pk=id)
    subject_id = exam.subject.id
    if is_teacher:
        exam = Exam.objects.get(pk=id, teacher=lgin_user.teacher)
        exam_student_is_finish = StudentExam.objects.filter(
            exam=exam,
            is_finish=True
        ).count()

        exam_form = ExamForm(request.POST or None, instance=exam)
        questions = Question.objects.filter(exam_c=exam)

        question_form = QuestionForm()

        if 'editExamBtn' in request.POST and exam_form.is_valid():
            exam_form.save()
            return redirect('exam', id=id)
        if 'deleteExamBtn' in request.POST:
            exam.delete()
            return redirect('subject', id=subject_id )
        if 'addQuestionBtn' in request.POST:

            question_title = request.POST['questionTitle']
            exam_question = exam
            new_question = Question(
                title = question_title,
                exam_c = exam_question
            )
            new_question.save()
            list_choices = ['choice1', 'choice2', 'choice3', 'choice4']
            for choice in list_choices:
                new_choice = request.POST[choice]
                if choice == request.POST['radioChoice']:
                    is_correct = True
                else:
                    is_correct = False
                new_exam_choice = Choice(
                    question_c = new_question,
                    title = new_choice,
                    is_correct = is_correct

                )
                new_exam_choice.save()
            return redirect('exam', id = id)
        if 'deleteQuestionBtn' in request.POST:
            question = Question.objects.get(pk=request.POST['deleteQuestionBtn'])
            question.delete()
            return redirect('exam', id=id)
        if 'updateQuestionBtn' in request.POST:
            question = Question.objects.get(pk=request.POST['updateQuestionBtn'])
            question.title = request.POST['questionTitle']
            try:
                old_correct_choice = Choice.objects.get(question_c=question, is_correct=True)
            except:
                return Http404

            choices = Choice.objects.filter(question_c=question)
            for choice in choices:
                choicePOST = "choice_title" + str(choice.id)
                choice.title = request.POST[choicePOST]
                choice.save()


            if request.POST['is_correct_check']:
                id = request.POST['is_correct_check']
                correct_choice = Choice.objects.get(pk=id)
                old_correct_choice.is_correct = False
                old_correct_choice.save()
                correct_choice.is_correct = True
                correct_choice.save()
            question.save()
            return redirect('exam', id = exam.id)

            



        context = {
            'exam': exam,
            'exam_form': exam_form,
            'questions': questions,
            'question_form': question_form,
            'exam_student_is_finish': exam_student_is_finish

        }

        return render(request, 'exam/exam_teacher.html', context )
    else:
        exam = Exam.objects.get(pk=id)
        
        if request.method == "POST" and "joinExamBtn" in request.POST:
            new_studentexam = StudentExam(
                student = request.user.student,
                exam=exam
            )
            new_studentexam.save()
            return redirect('student_exam', id=id)
        context = {
                    'exam': exam
                }
        
        try:
            student_exam = StudentExam.objects.get(
                student=request.user.student,
                exam=exam
            )
            context['is_join'] = False
            context['student_exam'] = student_exam
        except:
            if exam.status != 'open':
                context['is_join'] = False
            else:
                context['is_join'] = True


      
        return render(request, 'exam/exam_student.html', context)

    
@login_required
def student_exam(request,id):
    now = timezone.now()
    exam = Exam.objects.get(pk=id)

    studentexam = StudentExam.objects.get(
        student=request.user.student,
        exam=exam
    )
    questions = Question.objects.filter(exam_c=id)

    end_time = studentexam.joined + datetime.timedelta(minutes = exam.duration)

    limit_time = end_time - now
    if limit_time.days < 0:
        limit_minutes = 0
    else:
        limit_minutes = (limit_time.seconds % 3600) // 60
    if limit_minutes > 0:
        is_acept_test = True
    else:
        is_acept_test = False

    if is_acept_test:
        if request.method == "POST" and 'saveChoiceBtn' in request.POST:
            choice_id = "flexRadioDefault" + str(request.POST['saveChoiceBtn'])
            question = Question.objects.get(pk=request.POST['saveChoiceBtn'])
            choiced = request.POST[choice_id]
            choice = Choice.objects.get(pk=choiced)

            try:
                new_studentexamquestion = StudentExamQuestion.objects.get(
                    student_exam=studentexam,
                    question=question,
                )
            except:
                new_studentexamquestion = StudentExamQuestion(
                    student_exam=studentexam,
                    question=question
                )
            new_studentexamquestion.student_choice = choice
            new_studentexamquestion.save()
            return redirect('student_exam', id=id)
    
    if request.method == "POST" and 'finishExamBtn' in request.POST:
        studentexam.is_finish = True
        studentexam.save()
        return redirect('student_exam', id=id)
        
    context = {
        'questions': questions,
        'studentexam': studentexam,
        'end_time': end_time,
        'limit_time': limit_minutes,
        'is_acept_test': is_acept_test

    }
    return render(request, 'exam/student_join_exam.html', context)