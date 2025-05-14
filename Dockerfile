FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias desde la raíz
COPY requirements.txt .

# Instala las dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia solo la carpeta del backend al contenedor
COPY backend/ /app

# Expone el puerto que usará Uvicorn
EXPOSE 8000

# Comando para ejecutar la app (ajusta si usas otro archivo)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
