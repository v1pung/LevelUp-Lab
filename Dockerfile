FROM python:3.12
COPY requirements.txt .
RUN pip install -r requirements.txt
#WORKDIR /app
COPY . .
RUN apt install gcc -y
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s \
CMD python -c "import os, psycopg2; psycopg2.connect(os.getenv('DATABASE_URL')) or exit(1)"
CMD ["gunicorn", "-w", "2", "--bind", "0.0.0.0:8080", "run:application"]