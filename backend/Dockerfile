FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libpq-dev gcc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Rendre le script d'entrée exécutable
RUN chmod +x entrypoint.sh

EXPOSE 8000

# Le script d'entrée sera exécuté via la commande dans docker-compose.yml
CMD ["./entrypoint.sh"]
