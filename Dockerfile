# Используем официальный образ Python 3.8.3
FROM python:3.8.3-slim

RUN apt-get update
RUN apt-get install -y gcc libkrb5-dev

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости проекта
RUN pip install --no-cache-dir -r requirements.txt

# Указываем команду запуска
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--threads", "2", "main.wsgi:application"]

