# Generated by Django 4.1.7 on 2023-05-13 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_user_date_create'),
        ('lesson', '0004_alter_lesson_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='group',
            field=models.ManyToManyField(to='user.group'),
        ),
    ]
