LAB_LAT = 55.769798662546876
LAB_LON = 37.69094288756422
DURATION_COEF = 1.0
PRICE_PER_KILOMETER_OF_TRAVEL = 2

price_dict = {
    "underwater": 1,
    "surface": 2,
    "3d-model": 3,
    "report": 4,
    "defects": 5,
    "deffects-report": 6,
    "pier": 7,
    "big_pier": 8,
    "brige_supports": 9,
    "ship": 10,
    "barge": 11,
    "boat": 12,
    "research_surface": 13,
    "water_turbidity": 14,
    "flow": 15,
    "gravel": 16,
    "muddy": 17,
    "sand": 18,
}

service_options = {
    "Название проекта": "name",
    "Заказчик": "author",
    "Заказанные услуги": "service_group",
    "None1": "map_latitude",
    "None2": "map_longitude",
    "Характеристики объекта": "characteristic_group",
    "Площадь обследования, (кв.м)": "research_surface",
    "Мутность воды, (метров видимости)": "water_turbidity",
    "Скорость течения в области исследования, (м/с)": "flow",
    "Характеристики дна": "bottom_group",
    "Дата создания проекта": "created",
    "Дата выполнения проекта": "deadline",
    "Дополнительное описание": "additional_description",
    "Предварительная стоимость обследования, (руб.)": "price",
}

service_options2 = {
    "underwater": "Осмотр подводной части объека",
    "surface": "Осмотр надводной части объека",
    "3d-model": "Создание 3D-модели объекта",
    "report": "Составление отчета об осмотре",
    "defects": "Автоматический поиск дефектов",
    "deffects-report": "Создание отчета о дефектах",
    "pier": "Пирс",
    "big_pier": "Причал",
    "brige_supports": "Опоры мостов",
    "ship": "Корабль",
    "barge": "Баржа",
    "boat": "Катер",
    "muddy": "Илистое",
    "gravel": "Щебень",
    "sand": "Песок",
    "greenery": "Растительность"
}
