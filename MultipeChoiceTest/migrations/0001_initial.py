# Generated by Django 3.2.8 on 2021-11-03 02:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('is_correct', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('date_created', models.DateField(auto_now=True)),
                ('duration', models.IntegerField(verbose_name='Thời gian làm bài thi')),
                ('status', models.CharField(choices=[('wait', 'Chưa mở'), ('open', 'Đang mở'), ('close', 'Đã đóng')], default='wait', max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('exam_c', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MultipeChoiceTest.exam')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='StudentExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined', models.DateTimeField(auto_now=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MultipeChoiceTest.exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MultipeChoiceTest.student')),
            ],
            options={
                'unique_together': {('student', 'exam')},
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subjects', models.ManyToManyField(blank=True, to='MultipeChoiceTest.Subject', verbose_name='Môn thi')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentExamQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MultipeChoiceTest.question')),
                ('student_choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MultipeChoiceTest.choice')),
                ('student_exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MultipeChoiceTest.studentexam')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='subjects',
            field=models.ManyToManyField(blank=True, to='MultipeChoiceTest.Subject', verbose_name='Môn thi'),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='exam',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MultipeChoiceTest.subject'),
        ),
        migrations.AddField(
            model_name='exam',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MultipeChoiceTest.teacher'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question_c',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MultipeChoiceTest.question'),
        ),
    ]
