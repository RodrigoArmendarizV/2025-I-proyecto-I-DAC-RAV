# Usa una imagen base de Python
FROM python:3.12-slim

# Configuración del directorio de trabajo
WORKDIR /app

# Copia la carpeta app completa al contenedor
COPY app /app

# Instala las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 8080

# Comando para iniciar la aplicación
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
