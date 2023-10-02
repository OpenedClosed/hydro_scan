from datetime import datetime, timezone

from rest_framework import serializers

from orders.models import BottomGroup, CharacteristicGroup, Order
from users.serializers import CustomUserSerializer

from .help_functions import create_order_bottom, create_order_characteristic
from .service import calculate_price


class CharacteristicGroupSerializer(serializers.ModelSerializer):
    """Сериализатор создания и показа списка типов услуг"""

    class Meta:
        fields = '__all__'
        model = CharacteristicGroup


class BottomGroupSerializer(serializers.ModelSerializer):
    """Сериализатор создания и показа списка типов дна"""

    class Meta:
        fields = '__all__'
        model = BottomGroup


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор показа заказов"""
    author = CustomUserSerializer(read_only=True)
    price = serializers.IntegerField(read_only=True)
    characteristic_group = serializers.SlugRelatedField(
        many=True,
        queryset=CharacteristicGroup.objects.all(),
        slug_field='name'
    )
    bottom_group = serializers.SlugRelatedField(
        many=True,
        queryset=BottomGroup.objects.all(),
        slug_field='name'
    )

    def create(self, validated_data):
        price = calculate_price(
            validated_data,
        )
        characteristic_group = validated_data.pop('characteristic_group')
        bottom_group = validated_data.pop('bottom_group')

        order = Order.objects.create(
            **validated_data,
            price=price,
        )

        create_order_characteristic(characteristic_group, order)
        create_order_bottom(bottom_group, order)
        return order

    def update(self, instance, validated_data):
        characteristic_group = validated_data.pop('characteristic_group', None)
        bottom_group = validated_data.pop('bottom_group', None)
        order = instance

        if characteristic_group is not None:
            instance.ordercharacteristic.all().delete()
            create_order_characteristic(characteristic_group, order)

        if bottom_group is not None:
            instance.orderbottom.all().delete()
            create_order_bottom(bottom_group, order)

        return super(
            OrderSerializer, self
        ).update(instance, validated_data)

    def validate(self, data):
        deadline_date = data['deadline']
        current_data = datetime.now(timezone.utc)
        if deadline_date <= current_data:
            raise serializers.ValidationError(
                {'deadline': ('Не может быть раньше, чем текущее время')}
            )
        characteristic_groups = data['characteristic_group']
        id_of_characteristic_group = []
        for characteristic_group in characteristic_groups:
            if characteristic_group.id in id_of_characteristic_group:
                raise serializers.ValidationError(
                    {'characteristic_group': ('Типы объекта повторяются')}
                )
            id_of_characteristic_group.append(characteristic_group.id)

        bottom_groups = data['bottom_group']
        id_of_bottom_groups = []
        for bottom_group in bottom_groups:
            if bottom_group.id in id_of_bottom_groups:
                raise serializers.ValidationError(
                    {'bottom_group': ('Типы дна повторяются')}
                )
            id_of_bottom_groups.append(bottom_group.id)
        return data

    class Meta:
        fields = '__all__'
        model = Order
