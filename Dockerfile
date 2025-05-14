FROM python:3.11-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia solo el archivo de dependencias
COPY backend/requirements.txt .

# Instala las dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia todo el backend (incluyendo app, lógica y la carpeta db)
COPY backend /app/backend

# Expone el puerto
EXPOSE 8000

# Comando para iniciar el servidor
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
