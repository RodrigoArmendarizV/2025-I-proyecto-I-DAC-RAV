## App alternativa

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

Asegúrate de que `index.html` se encuentre en una carpeta llamada `templates`, junto con el archivo `app web.py`.

Posteriormente se debe correr el programa que se encuentra en la carpeta `app web` y finalmente, en tu buscador de confianza, ingresa el siguiente link `http://127.0.0.1:8080`.

La aplicación recibirá una imagen y al darle clic al botón `Analizar`, regresará la imagen junto con su predicción.

---

## Manejo de Errores
La API maneja errores utilizando códigos de estado HTTP estándar, asegurando una comunicación clara con el cliente:
- **400 - Solicitud Inválida:** Indica que la solicitud enviada por el cliente contiene errores, como subir una imagen no válida o un formato no soportado.
- **404 - Recurso No Encontrado:** Señala que el endpoint solicitado no existe o está mal especificado.
- **500 - Error Interno del Servidor:** Ocurre cuando hay un fallo inesperado durante el procesamiento en el servidor.
