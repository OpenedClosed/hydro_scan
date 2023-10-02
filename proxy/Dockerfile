# Используем базовый образ Nginx
FROM nginx:stable-alpine3.17-slim

# Установка Certbot
RUN apk update && apk add --no-cache certbot
RUN mkdir -p /certbot
RUN mkdir -p /app

# Скрипт для первого получения сертификата
COPY ./prod/certbot_first_ssl.sh /
RUN chmod +x /certbot_first_ssl.sh

# Скрипт для обновления сертификатов
COPY ./prod/certbot_renew.sh /etc/periodic/daily/
RUN chmod +x /etc/periodic/daily/certbot_renew.sh
