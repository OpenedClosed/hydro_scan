from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.viewsets import CreateReadViewSet

from .models import CustomUser
from .serializers import (
    ChangePasswordSerializer,
    CustomUserSerializer,
    SignUpSerializer,
    TokenSerializer,
)


class CustomUserViewSet(CreateReadViewSet):
    """Вьюсет данных пользователей"""
    queryset = CustomUser.objects.all().order_by('id')
    permission_classes = (AllowAny, )

    def get_serializer_class(self):
        if self.request.method in ('POST', ):
            return SignUpSerializer
        return CustomUserSerializer

    @action(methods=['get', ], detail=False,
            permission_classes=(IsAuthenticated, ))
    def me(self, request):
        """Метод, отвечающий за чтение пользователем
        собственных учетных данных"""
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post', ], detail=False,
            permission_classes=(IsAuthenticated, ))
    def set_password(self, request):
        """Метод, отвечающий за изменение пароля пользователем"""
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data.get('current_password')
        new_password = serializer.validated_data.get('new_password')
        user = request.user
        if user.password == old_password:
            user.password = new_password
            user.save()
            return Response(
                {"Пароль успешно изменен"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"current_password": "Введен неверный текущий пароль"},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST', ])
@permission_classes((AllowAny, ))
def get_token(request):
    """Вью-функция, отвечающая за получение зарегистрированным
    пользователем токена для доступа к сайту"""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    password = serializer.validated_data.get('password')
    new_user = get_object_or_404(CustomUser, email=email)

    if CustomUser.objects.filter(email=email, password=password).exists():
        if Token.objects.filter(user=new_user).exists():
            Token.objects.filter(user=new_user).delete()
        token = Token.objects.create(user=new_user)
        return Response({"auth_token": str(token)}, status=status.HTTP_200_OK)
    return Response(
        {"password": "Введен неверный пароль"},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST', ])
def delete_token(request):
    """Вью-функция, отвечающая за удаление токена"""
    request.auth.delete()
    return Response(
        {'Ваш токен успешно удален'},
        status=status.HTTP_200_OK
    )
