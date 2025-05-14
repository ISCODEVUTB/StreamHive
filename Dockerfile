FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia solo la carpeta del backend al contenedor
COPY backend/ /app

# Instala las dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expone el puerto por defecto de Uvicorn
EXPOSE 8000

# Comando para iniciar Uvicorn desde backend/app.py (sin reload)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
