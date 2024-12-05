from flask import Flask, request, jsonify, render_template, send_file
import matplotlib
matplotlib.use('Agg')
import tensorflow as tf
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing.image import img_to_array # type: ignore
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.ndimage import gaussian_filter
from io import BytesIO
import cv2
import sys
import logging

# Configurar logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Cargar el modelo
model = load_model('/app/cnn_neumonia.keras')

# Configuración del modelo
IMAGE_SIZE = (256, 256)
CLASSES = ['NORMAL', 'PNEUMONIA']  # Etiquetas de las clases

def preprocess_image(image):
    image = image.convert("L")
    image = image.resize(IMAGE_SIZE)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = image / 255.0
    return image

def generate_grad_cam_bounding_boxes(image, predictions):
    # Seleccionar la última capa convolucional
    last_conv_layer = [layer for layer in model.layers if isinstance(layer, tf.keras.layers.Conv2D)][-1]

    # Crear un modelo que mapea la entrada al último mapa de características y la salida del modelo
    grad_model = tf.keras.models.Model(inputs=model.input, outputs=[last_conv_layer.output, model.output])

    # Calcular los gradientes
    with tf.GradientTape() as tape:
        conv_outputs, preds = grad_model(image)
        loss = preds[0]

    grads = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # Ponderar las activaciones del mapa de características con los gradientes
    conv_outputs = conv_outputs[0]
    heatmap = tf.reduce_sum(pooled_grads * conv_outputs, axis=-1)

    # Aplicar ReLU y normalizar
    heatmap = tf.maximum(heatmap, 0) / tf.reduce_max(heatmap)

    # Convertir el heatmap a numpy
    heatmap = heatmap.numpy()
    heatmap_resized = tf.image.resize(
        tf.expand_dims(heatmap, axis=-1), IMAGE_SIZE, method='bilinear'
    ).numpy().squeeze()

    # Aplicar un filtro gaussiano para suavizar
    heatmap_smoothed = gaussian_filter(heatmap_resized, sigma=2)

    # Detectar componentes conectados para múltiples bounding boxes
    threshold = 0.6
    binary_heatmap = heatmap_smoothed > threshold
    num_labels, labels = cv2.connectedComponents(binary_heatmap.astype(np.uint8))

    bounding_boxes = []
    for label in range(1, num_labels):  # Ignorar el fondo (label 0)
        coords = np.argwhere(labels == label)
        y_min, x_min = coords.min(axis=0)
        y_max, x_max = coords.max(axis=0)
        bounding_boxes.append((x_min, y_min, x_max, y_max))

    # Convertir el heatmap en colores
    heatmap_color = plt.cm.jet(heatmap_smoothed)[:, :, :3] * 255

    # Superponer el heatmap a la imagen original
    original_image = image[0].squeeze() * 255
    original_image = np.uint8(original_image)
    superimposed_img = heatmap_color * 0.4 + np.stack((original_image,) * 3, axis=-1) * 0.6
    superimposed_img = np.clip(superimposed_img, 0, 255).astype('uint8')

    # Dibujar los bounding boxes
    fig, ax = plt.subplots()
    ax.imshow(superimposed_img.astype("uint8"))
    for x_min, y_min, x_max, y_max in bounding_boxes:
        ax.add_patch(
            plt.Rectangle(
                (x_min, y_min), x_max - x_min, y_max - y_min,
                fill=False, edgecolor='red', linewidth=2
            )
        )
    ax.axis("off")

    # Guardar la imagen como archivo temporal
    temp_image = BytesIO()
    plt.savefig(temp_image, format="png", bbox_inches="tight", pad_inches=0)
    temp_image.seek(0)
    plt.close(fig)
    return temp_image

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    """Procesa una solicitud de predicción."""
    if "file" not in request.files:
        return jsonify({"error": "No se subió ningún archivo"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    try:
        # Procesar la imagen
        image = Image.open(file)
        processed_image = preprocess_image(image)

        # Realizar predicción
        predictions = model.predict(processed_image)
        prediction_value = predictions[0][0]

        if prediction_value >= 0.5:
            predicted_class = "PNEUMONIA"
            confidence = prediction_value * 100
        else:
            predicted_class = "NORMAL"
            confidence = (1 - prediction_value) * 100

        # Mostrar diagnóstico en la terminal
        logger.info(f"Predicción: {predicted_class}, Confianza: {confidence:.2f}%")

        # Generar Grad-CAM
        grad_cam_image = generate_grad_cam_bounding_boxes(processed_image, predictions)

        # Guardar imagen temporalmente
        image_path = "/tmp/grad_cam.png"
        with open(image_path, "wb") as f:
            f.write(grad_cam_image.read())

        # Respuesta JSON con diagnóstico y enlace a la imagen
        return jsonify({
            "prediction": predicted_class,
            "confidence": f"{confidence:.2f}%",
            "image_path": image_path
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
