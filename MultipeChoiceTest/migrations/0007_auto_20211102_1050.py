# Generated by Django 3.2.8 on 2021-11-02 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MultipeChoiceTest', '0006_remove_question_choices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='title',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='exam',
            name='title',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='subject',
            name='title',
            field=models.TextField(),
        ),
    ]