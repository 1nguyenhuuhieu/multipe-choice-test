# Generated by Django 3.2.8 on 2021-11-08 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MultipeChoiceTest', '0005_alter_studentexam_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='duration',
            field=models.DurationField(verbose_name='Thời gian làm bài thi'),
        ),
    ]