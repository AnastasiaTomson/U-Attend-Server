from rest_framework import status, exceptions, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.conf import settings
from user.models import User, Teacher, Student, Group, generate_access_token, generate_refresh_token
from api.auth_api import registration_api, get_subgroups_from_group
from .serializers import RegistrationSerializer, LoginSerializer
import jwt


class AuthAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    login_serializer_class = LoginSerializer

    def post(self, request):
        login = request.data.get('login', '')
        password = request.data.get('password', '')
        is_staff = request.data.get('is_staff', False) == 'True'

        user = User.objects.filter(login__iregex=login)

        # Проверяем если есть пользователь и его статус указан правильно то авторизуемся
        if (is_staff and user.filter(teacher__isnull=False) or not is_staff and user.filter(
                student__isnull=False)) and user:
            if not user[0].check_password(password):
                status_response, response = registration_api(login, password, is_staff)
                if status_response:
                    user[0].set_password(password)
                    user[0].save()
            login_serializer = self.login_serializer_class(
                data={'login': user.first().login, 'password': password, 'is_staff': is_staff})
            login_serializer.is_valid(raise_exception=True)
            return Response(login_serializer.data, status=status.HTTP_201_CREATED)

        # Регистрируемся если что-то не так
        status_response, response = registration_api(login, password, is_staff)
        if status_response:
            if not user:
                serializer = self.serializer_class(data={'login': login, 'password': password})
                serializer.is_valid(raise_exception=True)
                user = serializer.save()
            else:
                user = user.first()
            access_token = generate_access_token(user, is_staff)
            refresh_token = generate_refresh_token(user, is_staff)
            if is_staff:
                Teacher.objects.create(**response, user=user)
            else:
                group = Group.objects.filter(name=response.get('group'))
                if not group:
                    status_code, groups = get_subgroups_from_group(response.get('group'))
                    if status_code == 500:
                        return Response({'error': groups}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    for item in groups:
                        group, create_status = Group.objects.get_or_create(**item)
                else:
                    group = group.last()
                response['group'] = group
                Student.objects.create(**response, user=user)
            return Response({'access_token': access_token, 'refresh_token': refresh_token},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'error': response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request):
    refresh_token = request.POST.get('refresh')
    if refresh_token is None:
        raise exceptions.AuthenticationFailed('Истек срок действия токена.')
    try:
        payload = jwt.decode(
            refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed('Токен не действителен.')

    user = User.objects.filter(id=payload.get('user_id')).first()
    if user is None:
        raise exceptions.AuthenticationFailed('Пользователь не найден')

    if not user.is_active:
        raise exceptions.AuthenticationFailed('Пользователь не активен')

    access_token = generate_access_token(user, payload.get('is_staff'))
    refresh_token = generate_refresh_token(user, payload.get('is_staff'))
    return Response({'access_token': access_token, 'refresh_token': refresh_token})
