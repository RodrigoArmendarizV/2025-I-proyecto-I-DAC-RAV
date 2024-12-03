# Usa una imagen base de Python
FROM python:3.12-slim

# Configuración del directorio de trabajo
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt /app/requirements.txt

# Instala las dependencias
RUN pip install -r /app/requirements.txt

# Copia todo lo demás
COPY app /app

# Expone el puerto
EXPOSE 8080

# Comando para iniciar la aplicación
CMD ["python", "/app/app.py"]
