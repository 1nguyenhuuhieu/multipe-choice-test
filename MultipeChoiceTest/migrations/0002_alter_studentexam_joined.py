# Generated by Django 3.2.8 on 2021-11-03 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MultipeChoiceTest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentexam',
            name='joined',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]