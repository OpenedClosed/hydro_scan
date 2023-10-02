import csv

from django.conf import settings
from django.core.management import BaseCommand

from orders.models import BottomGroup, CharacteristicGroup


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open(
            f"{settings.BASE_DIR}/orders/data/characteristic.csv",
            "r",
            encoding="utf-8",
        ) as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                name = row[0]
                CharacteristicGroup.objects.get_or_create(
                    name=name,
                )
            file.close()

        with open(
            f"{settings.BASE_DIR}/orders/data/bottom.csv",
            "r",
            encoding="utf-8",
        ) as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                name = row[0]
                BottomGroup.objects.get_or_create(
                    name=name,
                )
            file.close()

        self.stdout.write(self.style.SUCCESS(
            'Характеристика объекта и типы дна добавлены'))
