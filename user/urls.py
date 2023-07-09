from django.urls import path, include
from lesson.views import StudentAttendanceView, TeacherAttendanceView, ScanQrView, TeacherLessonAttendanceView
from .views import student_profile_view, teacher_profile_view

teacher_patterns = [
    path('profile/', teacher_profile_view),
    path('attendance/', TeacherAttendanceView.as_view()),
    path('attendance/<int:id>', TeacherLessonAttendanceView.as_view()),

]

student_patterns = [
    path('profile/', student_profile_view),
    path('attendance/', StudentAttendanceView.as_view()),
    path('scan_qr/<int:id>', ScanQrView.as_view()),
]

urlpatterns = [
    path('teacher/', include(teacher_patterns)),
    path('student/', include(student_patterns)),
]
