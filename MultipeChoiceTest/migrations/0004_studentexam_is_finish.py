# Generated by Django 3.2.8 on 2021-11-03 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MultipeChoiceTest', '0003_alter_studentexam_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentexam',
            name='is_finish',
            field=models.BooleanField(default=False),
        ),
    ]
