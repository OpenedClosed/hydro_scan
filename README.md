# Сервис HYDROSCAN

## Описание проекта<a name="description"></a>

Наша компания занимается визуальным осмотром гидротехнических сооружений (пирсы, причалы, опоры мостов, плотины, шлюзы, дамбы), а также плавучих средств (корабли, лодки, баржи) с возможностью создать 3D-модель объекта и выдавать отчет о дефектах. Для этого мы используем подводный аппарат (ПА) и беспилотный летательный аппарат (БПЛА) для осмотра объекта. С помощью подводного робота мы осматриваем и сканируем подводную часть гидротехнического объекта, а с помощью БПЛА — надводную часть. Компания выезжает на объект, осматривает его и делает 3D-модель с отчетом о дефектах.

Дизайн проекта [тут](https://www.figma.com/file/H3eBKfPRUuebVxlTy7jRmz/Веб-интерфейс-Гидроскана?type=design&node-id=0-1&mode=design)

## Стек<a name="stack"></a>

![Python](https://img.shields.io/badge/Python-3.11-blue) ![Django](https://img.shields.io/badge/Django-4.2-green) ![DRF](https://img.shields.io/badge/DRF-3.14-orange)


## Настройка и порядок работы

### Разработка при помощи Docker

Запустить и остановить сервис можнл следующими комманадми:
* Для режима разработчика

    Запуск
    ```
    docker compose -f dev.yml up -d --build
    ```

    Остановка
    ```
    docker compose -f dev.yml down
    ```

* Если код работает в production

    Запуск
    ```
    docker compose -f prod.yml up -d --build
    ```

    Остановка
    ```
    docker compose -f prod.yml down
    ```

Также будут полезны следующие комманды:

* Удаление всех контейнеров

    ```
    docker rm -f $(docker ps -aq)
    ```

* Удаление всех скаченных или собранных образов

    ```
    docker rmi -f $(docker images -aq)
    ```

* Удаление всех томов (пригодится если изменять параметры базы данных)

    ```
    docker volume rm -f $(docker volume ls -q)
    ```

* Очистка кеша и удаление ненужных данных, образов и тд

    ```
    docker system prune -f --volumes
    ```

### Установка и настройка DJANGO

Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Все последующие действия подразумевают, что вы находитесь в папке backend. Чтобы перейти в неё из корня проекта достаточно выполнить комманду:

```
cd backend
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать миграции:

```
python3 manage.py makemigrations
```

Применить миграции:

```
python3 manage.py migrate
```

Применить скрипт заполнения базы данных:

```
python3 manage.py db_script
```

Создать администратора django

```
python3 manage.py createsuperuser
```

Запустить проект:

```
python3 manage.py runserver
```

### Как запустить фронтенд

Установить yarn [тут](https://classic.yarnpkg.com/en/docs/install#windows-stable)

Перейти в директорию frontend

Выполнить команды в консоли: 

```
yarn
```

```
yarn quasar dev
```

### Команда проекта<a name="team"></a>

**Менеджер проекта:**

**Команда проекта:**

- Сергей Сандер ([@SerjioSA](https://t.me/SerjioSA), **[SerjioSA](https://github.com/SerjioSA)**) - frontend-разработчик, руководитель проекта

- Дмитрий Фирсов ([@samiyfs](https://t.me/samiyfs), **[OpenedClosed](https://github.com/OpenedClosed)**) - backend-разработчик

- Антон Солдаткин ([@soullesshorror](https://t.me/soullesshorror), **[Антон Солдаткин](https://github.com/AaronStoun)**) - backend-разработчик

- Серебрянников Олег ([@siraejka](https://t.me/siraejka), **[moprules](https://github.com/moprules)**) - fullstack-разработчик

- Чибизов Артем Евгеньевич ([@kukyrza](https://t.me/kukyrza), [ArtyomChibisov](https://github.com/ArtyomChibisov)) - backend-разработчик
