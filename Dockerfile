# Usar imagen base
FROM python:3.12-slim

# Configuración del directorio de trabajo
WORKDIR /app

# Copiar el código al contenedor
COPY app /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r /app/requirements.txt

# Comando para iniciar la aplicación
CMD ["python", "/app/app.py"]
