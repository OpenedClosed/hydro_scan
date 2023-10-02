"""Функции сервиса."""
import zoneinfo
from datetime import datetime
from math import atan2, cos, radians, sin, sqrt

from django.forms.models import model_to_dict
from fpdf import FPDF
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from hydro_scan import settings
from orders.models import Order
from users.models import CustomUser

from .constants import (
    DURATION_COEF,
    LAB_LAT,
    LAB_LON,
    PRICE_PER_KILOMETER_OF_TRAVEL,
    price_dict,
    service_options,
    service_options2,
)


def haversine(lat1, lon1, lat2, lon2):
    """Функция подсчета расстояния"""
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    R = 6371
    distance = R * c

    return distance


def calculate_price(
    obj,
    duration_coef=DURATION_COEF,
    price_per_kilometer_of_travel=PRICE_PER_KILOMETER_OF_TRAVEL,
    lab_lat=LAB_LAT,
    lab_lon=LAB_LON,
    price_dict=price_dict,
):
    """Функция подсчета цены"""
    final_price = 0
    data = obj
    lat2 = float(data["map_latitude"])
    lon2 = float(data["map_longitude"])
    d1 = datetime.now(zoneinfo.ZoneInfo(key='Europe/Moscow'))
    d2 = data["deadline"]
    delta = d2 - d1

    if(delta.days > 30):
        duration_coef = duration_coef + 0.1
    elif (delta.days <= 30 and delta.days > 20):
        duration_coef = duration_coef + 0.6
    else:
        duration_coef = duration_coef + 1.0

    distance = haversine(lab_lat, lab_lon, lat2, lon2)

    cost_of_services = 0
    characteristics = [
        ch_gr.name for ch_gr in obj['characteristic_group']]
    for characteristic in characteristics:
        cost_of_services += price_dict[characteristic]

    final_price += cost_of_services
    final_price += distance * price_per_kilometer_of_travel
    final_price = final_price * duration_coef

    return int(final_price)


pdfmetrics.registerFont(
    TTFont(
        'DejaVuSans',
        settings.BASE_DIR / 'fonts/DejaVuSans.ttf'))


def generate_pdf(user, order_id):
    """Функция формирования pdf отчета"""

    order = Order.objects.get(author=user.id, id=order_id)
    if not order:
        return ""

    # dict_from_order = order.values().first()
    dict_from_order = model_to_dict(order)

    pdf = FPDF()
    pdf.add_page()

    pdf.add_font(
        'DejaVuSans',
        '',
        settings.BASE_DIR / 'fonts/DejaVuSans.ttf',
        uni=True)

    pdf.image(str(settings.STATIC_ROOT / 'png/logo.png'), 150, 10, 33)

    pdf.set_font('DejaVuSans', size=40,)
    pdf.cell(200, 35, txt=('HYDROSCAN'), ln=1, align='C')

    for keys, values in service_options.items():
        for keys_of_json_dict, values_of_json_dict in dict_from_order.items():
            if values == keys_of_json_dict:
                if keys != 'None1' or keys != 'None2':
                    if keys_of_json_dict == 'map_latitude':
                        pdf.set_font('DejaVuSans', size=20)
                        pdf.cell(
                            200, 12, txt=('Расположение'), ln=1, align='L')
                        pdf.set_font('DejaVuSans', size=15)
                        pdf.cell(
                            200,
                            12,
                            txt=(
                                'Широта: ' + str(values_of_json_dict)),
                            ln=1,
                            align='L')
                    elif keys_of_json_dict == 'map_longitude':
                        pdf.set_font('DejaVuSans', size=15)
                        pdf.cell(
                            200,
                            12,
                            txt=('Долгота: ' + str(values_of_json_dict)),
                            ln=1,
                            align='L')
                    else:
                        if isinstance(values_of_json_dict, list):
                            pdf.set_font('DejaVuSans', size=20)
                            pdf.cell(200, 12, txt=str(keys), ln=1, align='L')
                            pdf.set_font('DejaVuSans', size=15)
                            for field in values_of_json_dict:
                                pdf.cell(
                                    200,
                                    12,
                                    txt=service_options2[field.name],
                                    ln=1,
                                    align='L'
                                )
                        else:
                            pdf.set_font('DejaVuSans', size=20)
                            pdf.cell(200, 12, txt=str(keys), ln=1, align='L')
                            pdf.set_font('DejaVuSans', size=15)
                            txt = str(values_of_json_dict)
                            if keys_of_json_dict == "author":
                                author = CustomUser.objects.get(
                                    id=values_of_json_dict)
                                txt = author.username
                            if keys_of_json_dict in ("deadline", "created"):
                                txt = values_of_json_dict.strftime("%Y-%m-%d")
                            pdf.cell(
                                200, 10, txt=txt,
                                ln=1, align='L'
                            )

    current_date = datetime.now(zoneinfo.ZoneInfo(
        key='Europe/Moscow')).strftime("%Y-%m-%d_T%H-%M-%S")
    file_name = (f'otchet_order_{order_id}_{current_date}.pdf')
    file_path = settings.MEDIA_ROOT / f'pdf/{file_name}'
    pdf.output(file_path)
    return file_path
