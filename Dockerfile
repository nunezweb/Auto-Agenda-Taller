# Etapa 1: Construir el frontend en Node.js
FROM node:20.0.0 AS frontend-build

WORKDIR /app

# Copia los archivos del frontend
COPY ./src/front ./front

# Instala las dependencias y construye el frontend
RUN cd ./front && npm install && npm run build

# Etapa 2: Configurar el entorno Python
FROM python:3.11-slim

# Crear y configurar el directorio de trabajo
WORKDIR /app

# Instalar las dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de requerimientos y luego instálalos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el contenido del proyecto al directorio de trabajo en el contenedor
COPY . .

# Copiar el build del frontend al directorio de recursos estáticos de Flask
COPY --from=frontend-build /app/front/build /app/src/static/

# Establecer las variables de entorno necesarias
ENV PYTHONUNBUFFERED=1

# Exponer el puerto en el que la aplicación correrá
EXPOSE 8080

# Comando por defecto para ejecutar la aplicación
CMD ["gunicorn", "wsgi:app", "--chdir", "/app/src", "--bind", "0.0.0.0:8080"]
