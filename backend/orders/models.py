from django.contrib.auth import get_user_model
from django.db import models

from users.models import CustomUser

from . constants import SERVICE_GROUP_CHOICES, STATUS_CHOICES


User = get_user_model()


class CharacteristicGroup(models.Model):
    """Модель типа услуги"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Тип объекта'
        verbose_name_plural = 'Типы объекта'
        ordering = ['id']

    def __str__(self):
        return self.name


class BottomGroup(models.Model):
    """Модель типа дна"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Тип дна'
        verbose_name_plural = 'Типы дна'
        ordering = ['id']

    def __str__(self):
        return self.name


def author_directory_path(instance, filename):
    return f"models/user_{instance.author.id}_{instance.id}_{filename}"


class Order(models.Model):
    """Модель заказа услуги"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название заказа'
    )
    service_group = models.CharField(
        max_length=200,
        choices=SERVICE_GROUP_CHOICES,
        verbose_name='Тип услуги'
    )
    map_latitude = models.CharField(
        max_length=200,
        verbose_name='Широта'
    )
    map_longitude = models.CharField(
        max_length=200,
        verbose_name='Долгота'
    )
    characteristic_group = models.ManyToManyField(
        CharacteristicGroup,
        through='OrderCharacteristic',
        related_name='orders',
        verbose_name='Характеристика объекта',
    )
    author = models.ForeignKey(
        CustomUser,
        related_name='orders',
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    research_surface = models.IntegerField(
        verbose_name='Площадь обследования'
    )
    water_turbidity = models.IntegerField(
        verbose_name='Видимость'
    )
    flow = models.IntegerField(
        verbose_name='Скорость течения воды'
    )
    bottom_group = models.ManyToManyField(
        BottomGroup,
        through='OrderBottom',
        related_name='orders',
        verbose_name='Тип дна',
    )
    price = models.IntegerField(
        verbose_name='Стоимость услуги'
    )
    deadline = models.DateTimeField(
        verbose_name='Крайний срок выполнения'
    )
    created = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата создания заказа'
    )
    additional_description = models.TextField(
        verbose_name='Дополнительное описание'
    )
    status = models.CharField(
        max_length=200,
        choices=STATUS_CHOICES,
        verbose_name='Статус заказа'
    )
    # model = models.CharField(
    #     max_length=200,
    #     unique=False,
    #     blank=True,
    #     verbose_name='Ссылка на 3D модель'
    # )

    model = models.FileField(
        upload_to=author_directory_path,
        default="models/empty_order.ply",
        verbose_name="Файл 3D модели")

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['id']

    def __str__(self):
        return self.name


class OrderCharacteristic(models.Model):
    """Вспомогательная модель,
    связывающая заказ и его группу
    объекта"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='ordercharacteristic',
        verbose_name='Заказ',
    )
    characteristic = models.ForeignKey(
        CharacteristicGroup,
        on_delete=models.CASCADE,
        related_name='ordercharacteristic',
        verbose_name='Тип объекта',
    )

    class Meta:
        verbose_name = 'Характеристика объекта'
        verbose_name_plural = 'Характеристики объекта'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'characteristic'],
                name='unique_characteristic_in_order'
            )
        ]


class OrderBottom(models.Model):
    """Вспомогательная модель,
    связывающая заказ и тип дна исследуемого объекта"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='orderbottom',
        verbose_name='Заказ',
    )
    bottom = models.ForeignKey(
        BottomGroup,
        on_delete=models.CASCADE,
        related_name='orderbottom',
        verbose_name='Тип дна',
    )

    class Meta:
        verbose_name = 'Тип дна в заказе'
        verbose_name_plural = 'Типы дна в заказе'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'bottom'],
                name='unique_bottom_in_order'
            )
        ]
