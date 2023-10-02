# Generated by Django 4.2 on 2023-07-23 09:08

from django.db import migrations, models

import orders.models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='model',
            field=models.FileField(
                default='/app/static/models/empty_order.ply',
                upload_to=orders.models.author_directory_path,
                verbose_name='Файл 3D модели'),
        ),
    ]