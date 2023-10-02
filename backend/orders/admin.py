from django.contrib import admin

from .models import (
    BottomGroup,
    CharacteristicGroup,
    Order,
    OrderBottom,
    OrderCharacteristic,
)


admin.site.register(CharacteristicGroup)
admin.site.register(BottomGroup)


class OrderCharacteristicInLine(admin.TabularInline):
    model = OrderCharacteristic
    extra = 0


class OrderBottomInLine(admin.TabularInline):
    model = OrderBottom
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderCharacteristicInLine, OrderBottomInLine, )
