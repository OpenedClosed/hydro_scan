import os
from pathlib import Path

from django.http import Http404, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import redirect

from hydro_scan import settings
from orders.models import BottomGroup, CharacteristicGroup, Order

from .pagination import LimitPageNumberPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    BottomGroupSerializer,
    CharacteristicGroupSerializer,
    OrderSerializer,
)
from .service import calculate_price, generate_pdf
from .viewsets import ReadViewSet


class OrderViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Заказ"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]
    queryset = Order.objects.all()
    pagination_class = LimitPageNumberPagination
    filter_backends = [DjangoFilterBackend, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @action(detail=False, methods=['GET'], name='my orders')
    def my(self, request, *args, **kwargs):
        queryset = Order.objects.filter(author=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], name='count the price')
    def price_count(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if (serializer.is_valid() is False):
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        obj = serializer.validated_data
        price = calculate_price(obj)
        return Response(dict([('price', price)]))


class CharacteristicViewSet(ReadViewSet):
    """Вьюсет модели Тип услуги"""
    serializer_class = CharacteristicGroupSerializer
    queryset = CharacteristicGroup.objects.all()
    pagination_class = None


class BottomViewSet(ReadViewSet):
    """Вьюсет модели Тип дна"""
    serializer_class = BottomGroupSerializer
    queryset = BottomGroup.objects.all()
    pagination_class = None

@api_view(['GET', ])
def download_report(request, order_id):
    """Вью-функция для загрузки pdf"""
    user = request.user
    if not user.is_authenticated:
        return redirect("/auth")
    file_path: Path = generate_pdf(user, order_id)
    if os.path.exists(file_path):
        response = HttpResponse()
        response["Content-Type"] = 'application/pdf'
        response["Content-Disposition"] = f'attachment; filename="{file_path.name}"'
        # Здесь media это не путь до папки media, это ссылка указанная в nginx как internal
        response['X-Accel-Redirect'] = f"/media/pdf/{file_path.name}"
        return response
    raise redirect("/404")

@api_view(['GET', ])
def download_3d_model(request, order_id):
    """Вью-функция для загрузки 3D модели"""
    user = request.user
    if not user.is_authenticated:
        return redirect("/auth")
    order = Order.objects.filter(author=user.id, id=order_id).values().first()
    file_path : Path = settings.MEDIA_ROOT / order["model"]
    if os.path.exists(file_path):
        response = HttpResponse()
        response["Content-Type"] = 'application/octet-stream'
        response["Content-Disposition"] = f'attachment; filename="{file_path.name}"'
        # Здесь media это не путь до папки media, это ссылка указанная в nginx как internal
        response['X-Accel-Redirect'] = f"/media/models/{file_path.name}"
        return response
    raise redirect("/404")
