# Generated by Django 3.2.8 on 2021-11-01 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MultipeChoiceTest', '0003_auto_20211101_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='questions',
            field=models.ManyToManyField(blank=True, null=True, to='MultipeChoiceTest.Question'),
        ),
    ]