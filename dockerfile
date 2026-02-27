# Dockerfile

# Usa una imagen oficial de Python. La versión "slim" es más pequeña.
FROM python:3.12-slim

# Instalar SSK cliente
RUN apt-get update && \
    apt-get install -y --no-install-recommends openssh-client

# Variables de entorno para Python:
# 1. Evita que Python escriba archivos .pyc en el disco.
ENV PYTHONDONTWRITEBYTECODE=1
# 2. Evita que Python bufferice la salida estándar (logs en tiempo real).
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo dentro del contenedor.
WORKDIR /app

# Copia el archivo de dependencias primero (aprovecha la caché de Docker).
COPY requirements.txt /app/

# Instala las dependencias del proyecto.
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copia el resto del código del proyecto al directorio de trabajo.
COPY . /app/

# Expone el puerto en el que Django correrá dentro del contenedor.
EXPOSE 8000

# Comando para ejecutar el servidor de desarrollo de Django.
# Escucha en todas las interfaces (0.0.0.0) para que sea accesible desde el host.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]