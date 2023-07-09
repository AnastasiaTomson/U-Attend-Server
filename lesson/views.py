from api.schedule_api import get_schedule, get_today_timetable, get_lesson_now
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
import datetime
from .models import Lesson, Attendance
from user.models import Group
import re
from django.db import IntegrityError
from django.db.models import Q


class GetTimetable(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TimetableSerializer

    def get(self, request):
        try:
            teacher = request.user.teacher
            if teacher:
                timetable = get_schedule(teacher.get_full_name()).get('timetable')
                today_timetable = get_today_timetable(timetable)
                return Response(today_timetable, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': 'Ошибка'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetLesson(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TimetableSerializer

    def get(self, request, id):
        try:
            lesson = Lesson.objects.get(id=id)
            return Response(self.serializer_class(lesson).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Ошибка'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateQRView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TimetableSerializer

    def post(self, request):
        try:
            teacher = request.user.teacher
            if teacher:
                weekday = 5
                '''datetime.datetime.today().weekday() + 1'''
                week = int(1 if request.data.get('week') == 'Четная неделя' else 2)
                type_lesson = {i.label: i.value for i in Lesson.Types}[request.data.get('type')]
                sync = {i.label: i.value for i in Lesson.Syncs}[request.data.get('sync')]
                print(request.data.get('groups').split(','))
                lesson, status_create = Lesson.objects.get_or_create(weekday=weekday, week=week,
                                                                     time=request.data.get('time'),
                                                                     subject=request.data.get('subject'), type=type_lesson,
                                                                     place=request.data.get('place'),
                                                                     building=request.data.get('building'),
                                                                     room=request.data.get('room'), sync=sync,
                                                                     teacher=teacher)
                for group in request.data.get('groups').split(','):
                    re_group = re.search(r"([^\s()]+)(?:\s\(([^()]*)\))?", group)
                    if re_group:
                        row_group = re_group.groups()
                        subgroup = row_group[1]
                        group_object, status_code = Group.objects.get_or_create(name=row_group[0].upper(), subgroup=subgroup)
                        if group_object not in lesson.group.all():
                            lesson.group.add(group_object)
                serializer = self.serializer_class(lesson)
                print(lesson)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            pass
            print(e)
        return Response({'error': 'Ошибка'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ScanQrView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        try:
            user = request.user.student
            lesson = Lesson.objects.get(id=id)
            if user.group in lesson.group.all() and lesson.check_time():
                Attendance.objects.create(student=user, lesson=lesson)
                return Response({'status': True, 'message': 'Вы отметились на занятии'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': False, 'message': 'Не удалось отметиться'},
                                status=status.HTTP_200_OK)
        except IntegrityError as e:
            return Response({'status': False, 'message': 'Вы уже отметились на занятии'},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': 'Ошибка'}, status=status.HTTP_500_INTERNALq_SERVER_ERROR)


class StudentAttendanceView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AttendanceStudentSerializer

    def get(self, request):
        try:
            user = request.user.student
            print(request.user.date_create)
            lessons = Lesson.objects.filter(group=user.group, date__gte=request.user.date_create).order_by('-date')
            serializer = self.serializer_class(lessons, many=True)
            for lesson in serializer.data:
                is_attend = True if Attendance.objects.filter(lesson_id=lesson['id'], student=user).count() else False
                lesson['is_attend'] = is_attend
            json = attend_group_by_date(serializer.data)
            return Response(json, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': 'Ошибка'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TeacherAttendanceView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AttendanceTeacherSerializer

    def get(self, request):
        try:
            user = request.user.teacher
            lessons = Lesson.objects.filter(teacher=user).order_by('-date')
            serializer = self.serializer_class(lessons, many=True)
            json = attend_group_by_date(serializer.data)
            return Response(json, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': 'Ошибка'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def attend_group_by_date(data):
    last_date = ''
    lesson_dict = {}
    json = []
    for lesson in data:
        if last_date != lesson['date']:
            last_date = lesson['date']
            if lesson_dict:
                json.append(lesson_dict)
            lesson_dict = {'date': last_date}
        if last_date == lesson['date']:
            if 'lessons' in lesson_dict.keys():
                lesson_dict['lessons'].append(lesson)
            else:
                lesson_dict['lessons'] = [lesson]
        if not json and lesson_dict:
            json.append(lesson_dict)
    return json

class TeacherLessonAttendanceView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StudentAttendanceSerializer
    serializer_student_class = StudentAttendanceSerializer

    def get(self, request, id):
        try:
            lesson = Lesson.objects.get(id=id)
            attends = Student.objects.filter(group__in=lesson.group.all()).order_by('surname')
            serializer = self.serializer_class(attends, many=True)
            for student in serializer.data:
                student['is_attend'] = Student.objects.filter(students__lesson_id=id, id=student.get('id')).exists()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Ошибка'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, id):
        try:
            lesson = Lesson.objects.get(id=id)
            students_id = request.data.get('students_id')
            for student_id in students_id:
                attend, status_object = Attendance.objects.get_or_create(student_id=int(student_id), lesson=lesson)
                if not status_object:
                    attend.delete()
            attends = Student.objects.filter(group__in=lesson.group.all())
            serializer = self.serializer_class(attends, many=True)
            for student in serializer.data:
                student['is_attend'] = Student.objects.filter(students__lesson_id=id, id=student.get('id')).exists()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'status': False, 'message': 'Ошибка'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
