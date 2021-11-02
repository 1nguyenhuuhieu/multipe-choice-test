from django.contrib.auth import login, logout
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

from django.contrib import messages

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
        except:
            subject_form = TeacherForm(instance=request.user.student)



    context = {

        'user_form': user_form,
        'teacher_form': subject_form,

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
            'question_form': question_form

        }

        return render(request, 'exam/exam_teacher.html', context )
    else:
        context = {

            'exam': exam

        }
        return render(request, 'exam/exam_student.html', context)