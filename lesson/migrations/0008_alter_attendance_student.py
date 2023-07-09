# Generated by Django 4.1.7 on 2023-05-20 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_user_date_create'),
        ('lesson', '0007_alter_lesson_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='user.student'),
        ),
    ]
