from django.urls import path

from .views import GetTimetable, GetLesson, CreateQRView, ScanQrView

urlpatterns = [
    path('lesson/', GetTimetable.as_view()),
    path('lesson/<int:id>', GetLesson.as_view()),
    path('create_lesson/', CreateQRView.as_view()),
]
