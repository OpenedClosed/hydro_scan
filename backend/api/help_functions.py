"""Вспомогательные функции, сокращающие код"""
from orders.models import OrderBottom, OrderCharacteristic


def create_order_characteristic(characteristics, order):
    """Вспомогательная функция для создание связи
    между заказом и его типом услуги"""
    for characteristic in characteristics:
        OrderCharacteristic.objects.bulk_create([
            OrderCharacteristic(
                order=order,
                characteristic=characteristic
            )
        ])


def create_order_bottom(bottoms, order):
    """Вспомогательная функция для создание связи
    между заказом и его типом дна"""
    for bottom in bottoms:
        OrderBottom.objects.bulk_create([
            OrderBottom(
                order=order,
                bottom=bottom
            )
        ])
