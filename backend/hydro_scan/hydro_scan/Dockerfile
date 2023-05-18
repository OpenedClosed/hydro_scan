FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN pip3 install -r /app/requirements.txt --no-cache-dir

CMD ["gunicorn", "hydro_scan.wsgi:application", "--bind", "0:8000" ] 