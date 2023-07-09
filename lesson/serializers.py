from rest_framework import serializers
from user.models import User, Student
from lesson.models import Lesson, Attendance
from user.serializers import TeacherSerializer
from user.models import Group
from user.serializers import StudentSerializer


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class TimetableSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(source='group', many=True)
    weekday = serializers.CharField(source='get_weekday_display')
    week = serializers.CharField(source='get_week_display')
    type = serializers.CharField(source='get_type_display')
    sync = serializers.CharField(source='get_sync_display')
    date = serializers.DateField(format="%d.%m.%Y")
    teacher = serializers.StringRelatedField()

    class Meta:
        model = Lesson
        fields = ['id', 'week', 'time', 'subject', 'type', 'place', 'building', 'room', 'sync', 'date',
                  'weekday', 'teacher', 'groups']


class AttendanceStudentSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(source='group', many=True)
    weekday = serializers.CharField(source='get_weekday_display')
    week = serializers.CharField(source='get_week_display')
    type = serializers.CharField(source='get_type_display')
    sync = serializers.CharField(source='get_sync_display')
    date = serializers.DateField(format="%d.%m.%Y")
    teacher = serializers.StringRelatedField()
    is_attend = serializers.BooleanField(default=False)

    class Meta:
        model = Lesson
        fields = ['id', 'week', 'time', 'subject', 'type', 'place', 'building', 'room', 'sync', 'date',
                  'weekday', 'teacher', 'groups', 'is_attend']


class AttendanceTeacherSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(source='group', many=True)
    weekday = serializers.CharField(source='get_weekday_display')
    week = serializers.CharField(source='get_week_display')
    type = serializers.CharField(source='get_type_display')
    sync = serializers.CharField(source='get_sync_display')
    date = serializers.DateField(format="%d.%m.%Y")
    teacher = serializers.StringRelatedField()
    count_student_attend = serializers.IntegerField(default=0)

    class Meta:
        model = Lesson
        fields = ['id', 'week', 'time', 'subject', 'type', 'place', 'building', 'room', 'sync', 'date',
                  'weekday', 'teacher', 'groups', 'count_student_attend']
                  

class StudentAttendanceSerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField()
    is_attend = serializers.BooleanField(default=False)

    class Meta:
        model = Student
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    lesson = TimetableSerializer()
    student = StudentSerializer()

    class Meta:
        model = Attendance
        fields = '__all__'
