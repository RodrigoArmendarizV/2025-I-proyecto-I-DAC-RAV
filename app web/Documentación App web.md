# Documentación General de la App web

1. [App web](#app-alternativa)
   - [Características](#características)
   - [Requisitos del sistema](#requisitos-del-sistema)
   - [Uso de la aplicación](#uso-de-la-aplicación)
2. [Manejo de errores](#manejo-de-errores)

### Fecha de Actualización
Última actualización: 05-12-2024

## App web

Esta es una aplicación web desarrollada con Flask que utiliza el mismo modelo para detectar neumonía a partir de imágenes médicas. La aplicación permite cargar imágenes, analizar su contenido y visualizar áreas relevantes mediante *Grad-CAM*.

### **Características**

- Clasificación binaria: **NORMAL** o **PNEUMONIA**.
- Generación de mapas de calor (*Grad-CAM*) para visualizar áreas relevantes en la imagen.
- Visualización interactiva a través de una página web.
- Respuesta en formato de imagen y encabezados HTTP con el nivel de confianza del modelo.

### **Requisitos del sistema**

- Python 3.12 o superior.
- Las siguientes librerías de Python:
  - `Flask`
  - `TensorFlow`
  - `Pillow`
  - `Matplotlib`
  - `SciPy`
  - `OpenCV`
  - `NumPy`
 
### Uso de la aplicación

Para poder usar esta aplicación es bastante simple, primero, se debe clonar el repositorio:
```bash
git clone https://github.com/RodrigoArmendarizV/2025-I-proyecto-I-DAC-RAV.git
cd 2025-I-proyecto-I-DAC-RAV
```

Es indispensable descargar el modelo y se puede hacer con el siguiente enlace:

[Descargar modelo cnn_neumonia.keras](https://drive.google.com/file/d/1lIucaM2YqiQma1Z3UGR28jJuoSuR9XmT/view?usp=sharing)

Asegúrate de que `index.html` se encuentre en una carpeta llamada `templates`, junto con el archivo `app web.py`. En la línea 18 del archivo `app web.py` se encontrará el siguiente texto `model = load_model('/ruta/al/archivo/cnn_neumonia.keras')` donde es indispensable proporcionar la ruta correcta del modelo para el funcionamiento de la app.

Posteriormente se debe correr el archivo `app web.py` en un editor de código fuente y finalmente, en tu buscador de confianza, ingresa el siguiente enlace: `http://127.0.0.1:8080`

Si se está ejecutando correctamente debe salir el siguiente texto en la terminal:
```bash
 * Serving Flask app 'app web'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://<your-local-ip>:8080
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: <PIN>
```

La aplicación recibirá una imagen y al darle clic al botón `Analizar`, regresará la imagen junto con su predicción.

---

## Manejo de Errores
La app maneja errores utilizando códigos de estado HTTP estándar, asegurando una comunicación clara con el cliente:
- **400 - Solicitud Inválida:** Indica que la solicitud enviada por el cliente contiene errores, como subir una imagen no válida o un formato no soportado.
- **404 - Recurso No Encontrado:** Señala que el endpoint solicitado no existe o está mal especificado.
- **500 - Error Interno del Servidor:** Ocurre cuando hay un fallo inesperado durante el procesamiento en el servidor.
