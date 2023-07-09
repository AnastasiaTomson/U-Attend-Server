# Generated by Django 4.1.7 on 2023-04-22 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_user_date_create'),
        ('lesson', '0002_alter_lesson_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='datetime_check',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together={('student', 'lesson')},
        ),
    ]
