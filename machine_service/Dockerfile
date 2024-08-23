
# образ на основе которого создаём контейнер
FROM python:latest
# рабочая директория внутри проекта
WORKDIR /app
# копируем содержимое текущей папки в контейнер
COPY . /app
# копируем и устанавливаем зависимости
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# переменные окружения для python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# выполняем миграции

CMD  python manage.py migrate \
     && pip install --upgrade pip \
     && python manage.py runserver 0.0.0.0:8000

