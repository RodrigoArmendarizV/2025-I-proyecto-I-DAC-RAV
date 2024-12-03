# Usa una imagen base de Python
FROM python:3.12-slim

# Configuración del directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY app.py /app/
COPY templates/ /app/templates/
COPY cnn_neumonía.keras /app/

# Instala las dependencias
RUN pip install -r requirements.txt

# Expone el puerto
EXPOSE 8080

# Comando para iniciar la aplicación
CMD ["python", "app.py"]
