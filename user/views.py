from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import HttpResponseRedirect, JsonResponse
from .serializers import StudentSerializer, TeacherSerializer
from .models import Teacher, Student


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_profile_view(request):
    student = Student.objects.filter(user=request.user).first()
    if student:
        serializer = StudentSerializer(student)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Ошибка'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def teacher_profile_view(request):
    teacher = Teacher.objects.filter(user=request.user).first()
    if teacher:
        serializer = TeacherSerializer(teacher)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Ошибка'})

