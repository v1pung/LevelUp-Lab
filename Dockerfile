# FROM python:3.12
#
# COPY requirements.txt .
# RUN apt install gcc -y
# RUN pip install -r requirements.txt
#
# #WORKDIR /app
# COPY . .
# EXPOSE 8080
# HEALTHCHECK --interval=30s --timeout=3s \
#
# # CMD python -c "import os, psycopg2; psycopg2.connect(os.getenv('DATABASE_URL')) or exit(1)"
# RUN if [ ! -d "migrations" ]; then \
#       flask db init && \
#       flask db migrate -m "Initial migration"; \
#     fi
# CMD ["sh", "-c", "flask", "db", "upgrade"]
#
# CMD ["gunicorn", "-w", "2", "--bind", "0.0.0.0:8080", "run:application"]

FROM python:3.12

# Установка зависимостей
RUN apt-get update && apt-get install -y gcc

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование приложения
COPY . .

# Инициализация миграций
RUN flask db init || true  # Пропускаем ошибку, если миграции уже инициализированы

EXPOSE 8080

# Команда запуска (объединённая)
CMD ["sh", "-c", "flask db migrate; flask db upgrade; gunicorn -w 2 --bind 0.0.0.0:8080 run:application"]