# Usa una imagen base de Python
FROM python:3.12-slim

# Configuración del directorio de trabajo
WORKDIR /app

# Copia la carpeta app completa al contenedor
COPY app /app

# Instala las dependencias desde requirements.txt
RUN pip install -r /app/requirements.txt

# Expone el puerto
EXPOSE 8080

# Comando para iniciar la aplicación
CMD ["python", "/app/app.py"]
