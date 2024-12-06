
# Documentación General de la API

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Requisitos Previos](#requisitos-previos)
3. [Instalación](#instalación)
   - [Clonación del Repositorio](#clonación-del-repositorio)
   - [Descargar el modelo](#descargar-el-modelo)
4. [Uso de Docker](#uso-de-docker)
   - [Construcción de la Imagen](#construcción-de-la-imagen)
   - [Ejecución del Contenedor](#ejecución-del-contenedor)
   - [Detener y Eliminar Contenedores](#detener-y-eliminar-contenedores)
5. [Endpoints de la API](#endpoints-de-la-api)
   - [POST /predict](#post-predict)
6. [App alternativa](#app-alternativa)
   - [Características](#características)
   - [Requisitos del sistema](#requisitos-del-sistema)
   - [Uso de la aplicación](#uso-de-la-aplicación)
8. [Manejo de errores](#manejo-de-errores)

---

## Introducción
Esta API permite analizar radiografías de tórax para detectar neumonía utilizando redes neuronales convolucionales. Genera un Grad-CAM para visualizar las áreas más relevantes en las imágenes analizadas.

Es ideal para integrarse en sistemas médicos que requieran un diagnóstico automatizado complementario.

### Fecha de Actualización
Última actualización: 02-12-2024

---

## Requisitos Previos
- Docker y Docker Compose instalados.
- Git instalado.
- Python 3.12 (para desarrollo).
- Configuración básica del sistema operativo.

## Instalación

### Clonación del Repositorio
Clona el repositorio del proyecto:
```bash
git clone https://github.com/RodrigoArmendarizV/2025-I-proyecto-I-DAC-RAV.git
cd 2025-I-proyecto-I-DAC-RAV
```

---

## Descargar el modelo

El modelo necesario para ejecutar la API es bastante pesado y no está incluido directamente en el repositorio pero se puede descargar en el siguiente enlace:
 
[Descargar modelo cnn_neumonia.keras](https://drive.google.com/file/d/1lIucaM2YqiQma1Z3UGR28jJuoSuR9XmT/view?usp=sharing)

Guarda el archivo en la ubicación `/app/cnn_neumonía.keras` independientemente del método que se decida usar.

---
 
## Uso de Docker

### Construcción de la Imagen
Construye la imagen de Docker:
```bash
docker build -t neumonia-api .
```

### Ejecución del Contenedor
Inicia el contenedor con Docker:
```bash
docker run -d -p 8080:8080 neumonia-api
```
Accede a la interfaz de usuario en `http://127.0.0.1:8080/predict`

### Detener y Eliminar Contenedores
Para detener un contenedor:
```bash
docker stop <container_id>
```
Para eliminarlo:
```bash
docker rm <container_id>
```
---

## Endpoints de la API

### POST /predict
**Descripción:** Clasifica una imagen para la detección de neumonía a partir de radiografías de tórax.

**Request Body:**
- `file` (archivo): Archivo de imagen de la radiografía (formato JPEG o JPG).

**Ejemplo:**
```bash
curl -X POST -F "file=@/radiografia.jpeg" http://127.0.0.1:8080/predict/ --output grad_cam.png
```

**Response:**
La respuesta consta de dos partes:
1. Un archivo de imagen Grad-CAM en formato `.png`, que se guarda como `grad_cam.png`.
2. Un objeto JSON con la predicción y el nivel de confianza. Para acceder a la predicción se hace de la siguiente manera:

```bash
docker logs <container_id>
```
Donde el formato de respuesta es:
```bash
Predicción: NORMAL, Confianza: 95.34%
```

---

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
