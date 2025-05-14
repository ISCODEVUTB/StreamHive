# Imagen base con Python 3.11
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de dependencias
COPY backend/requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente del backend
COPY backend/ .

# Exponer el puerto en el que la aplicación se ejecutará
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["python", "app.py"]
