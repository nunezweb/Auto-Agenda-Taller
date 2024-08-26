# Etapa 1: Construir el frontend en Node.js (si tienes un frontend en React)
FROM node:20.0.0 AS frontend-build

WORKDIR /app

# Copia los archivos de frontend
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

# Copiar el archivo de requerimientos y instalar las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código fuente
COPY . .

# Si tienes un frontend estático, copia el build al directorio de recursos estáticos de Flask
COPY --from=frontend-build /app/front/build /app/src/static/

# Establecer las variables de entorno
ENV PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    DATABASE_URL=${DATABASE_URL} \
    JWT_SECRET=${JWT_SECRET} \
    CORS_ORIGIN=${CORS_ORIGIN}

# Exponer el puerto para la aplicación Flask
EXPOSE 8080

# Comando para iniciar la aplicación
CMD ["gunicorn", "wsgi:app", "--chdir", "/app/src", "--bind", "0.0.0.0:8080"]
