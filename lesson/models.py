from django.db import models
from user.models import Group, Student, Teacher
from datetime import datetime


class Lesson(models.Model):
    WEEKS = (
        (1, 'Пн'),
        (2, 'Вт'),
        (3, 'Ср'),
        (4, 'Чт'),
        (5, 'Пт'),
        (6, 'Сб'),
        (7, 'Вс'),
    )
    TYPE_WEEKS = (
        (1, 'Нечетная неделя'),
        (2, 'Четная неделя')
    )

    class Types(models.IntegerChoices):
        PR = 1, "пр. занятие"
        LEC = 2, "лекция"

    class Syncs(models.IntegerChoices):
        SYNC = 1, "синхронно"
        ASYNC = 2, "асинхронно"

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятие'

    weekday = models.SmallIntegerField(choices=WEEKS)
    week = models.SmallIntegerField(choices=TYPE_WEEKS)
    date = models.DateField(auto_now_add=True)
    time = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    type = models.SmallIntegerField(choices=Types.choices)
    place = models.CharField(max_length=255)
    building = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    sync = models.SmallIntegerField(choices=Syncs.choices)
    group = models.ManyToManyField(Group)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)

    def check_time(self):
        start_time, end_time = self.time.split('-')
        start_time = datetime.strptime(start_time, "%H:%M").time()
        end_time = datetime.strptime(end_time, "%H:%M").time()
        current = datetime.strptime('13:30', "%H:%M").time()
        return start_time <= current <= end_time


class Attendance(models.Model):
    class Meta:
        verbose_name_plural = 'Посещаемость'
        verbose_name = 'Посещаемость'
        unique_together = ('student', 'lesson')

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='students')
    datetime_check = models.DateTimeField(auto_now_add=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
