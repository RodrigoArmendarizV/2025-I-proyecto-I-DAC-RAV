from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from scipy.ndimage import gaussian_filter
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import cv2

# Crear la app de FastAPI
app = FastAPI()

# Configuración de CORS (opcional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

# Cargar el modelo
model = load_model('/app/cnn_neumonia.keras')

# Configuración del modelo
IMAGE_SIZE = (256, 256)
CLASSES = ['NORMAL', 'PNEUMONIA']  # Etiquetas de las clases

def preprocess_image(image):
    image = image.convert('L')
    image = image.resize(IMAGE_SIZE)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = image / 255.0
    return image

def generate_grad_cam_bounding_boxes(image, predictions):
    last_conv_layer = [layer for layer in model.layers if isinstance(layer, tf.keras.layers.Conv2D)][-1]
    grad_model = tf.keras.models.Model(inputs=model.input, outputs=[last_conv_layer.output, model.output])

    with tf.GradientTape() as tape:
        conv_outputs, preds = grad_model(image)
        loss = preds[0]

    grads = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]
    heatmap = tf.reduce_sum(pooled_grads * conv_outputs, axis=-1)
    heatmap = tf.maximum(heatmap, 0) / tf.reduce_max(heatmap)
    heatmap = heatmap.numpy()

    heatmap_resized = tf.image.resize(
        tf.expand_dims(heatmap, axis=-1), IMAGE_SIZE, method='bilinear'
    ).numpy().squeeze()
    heatmap_smoothed = gaussian_filter(heatmap_resized, sigma=2)

    threshold = 0.6
    binary_heatmap = heatmap_smoothed > threshold
    num_labels, labels = cv2.connectedComponents(binary_heatmap.astype(np.uint8))

    bounding_boxes = []
    for label in range(1, num_labels):
        coords = np.argwhere(labels == label)
        y_min, x_min = coords.min(axis=0)
        y_max, x_max = coords.max(axis=0)
        bounding_boxes.append((x_min, y_min, x_max, y_max))

    heatmap_color = plt.cm.jet(heatmap_smoothed)[:, :, :3] * 255
    original_image = image[0].squeeze() * 255
    original_image = np.uint8(original_image)
    superimposed_img = heatmap_color * 0.4 + np.stack((original_image,) * 3, axis=-1) * 0.6
    superimposed_img = np.clip(superimposed_img, 0, 255).astype('uint8')

    fig, ax = plt.subplots()
    ax.imshow(superimposed_img.astype('uint8'))
    for x_min, y_min, x_max, y_max in bounding_boxes:
        ax.add_patch(
            plt.Rectangle(
                (x_min, y_min), x_max - x_min, y_max - y_min,
                fill=False, edgecolor='red', linewidth=2
            )
        )
    ax.axis('off')

    temp_image = BytesIO()
    plt.savefig(temp_image, format='png', bbox_inches='tight', pad_inches=0)
    temp_image.seek(0)
    plt.close(fig)
    return temp_image

@app.post('/predict/')
async def predict(file: UploadFile = File(...)):
    try:
        print('Inicio del procesamiento de la imagen.')
        image = Image.open(file.file)
        print('Imagen cargada correctamente.')
        
        processed_image = preprocess_image(image)
        print(f'Imagen procesada: {processed_image.shape}')

        predictions = model.predict(processed_image)
        print(f'Predicciones realizadas: {predictions}')

        prediction_value = predictions[0][0]
        print(f'Valor de la predicción: {prediction_value}')

        if prediction_value >= 0.5:
            predicted_class = 'PNEUMONIA'
            confidence = prediction_value * 100
            confidence_message = f'Predicción: {predicted_class}, Confianza: {confidence:.2f}'
        else:
            predicted_class = 'NORMAL'
            confidence = (1 - prediction_value) * 100
            confidence_message = f'Predicción: {predicted_class}, Confianza: {confidence:.2f}'

        print(confidence_message)

        grad_cam_image = generate_grad_cam_bounding_boxes(processed_image, predictions)
        print('Grad-CAM generado correctamente.')

        headers = {
            'X-Prediction': predicted_class,
            'X-Confidence': confidence_message,
        }

        return StreamingResponse(grad_cam_image, media_type='image/png', headers=headers)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
