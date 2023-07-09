from rest_framework import serializers
from user.models import User, Student, Group, Teacher, generate_access_token, generate_refresh_token
from django.contrib.auth import authenticate
import secrets


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        exclude = ['id', 'user']


class StudentSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Student
        exclude = ['id', 'user']
