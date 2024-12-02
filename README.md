#  ![Logo Facultad de Ciencias](images/logoFC85.png) Proyecto - Detector de Neumonía.

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![TensorFlow Version](https://img.shields.io/badge/TensorFlow-2.18-orange.svg)](https://www.tensorflow.org/)

[Video Demo](https://drive.google.com/file/d/1a__4Ig-tmgPqYBSufVAHB0RoLGicGaIw/view?usp=drive_link)

[Frontend en Github pages](https://jrbeduardo.github.io/proyecto-malaria/)

## Integrantes:  

- Diego Arias Cabrera
- Rodrigo Armendáriz Viegas

## Entegrables:

1. [Memoria Técnica](dev_model/MEMORIA-TECNICA.md)
1. [Documentación API](app/documentacion-api.md)

## Contexto

La neumonía es una enfermedad respiratoria grave que afecta a millones de personas en todo el mundo y representa una de las principales causas de mortalidad, especialmente en niños menores de cinco años y adultos mayores. Su impacto es más severo en regiones con acceso limitado a la atención médica. El objetivo principal es mejorar el diagnóstico temprano y la precisión en su detección mediante herramientas avanzadas de aprendizaje automático, brindando apoyo a los profesionales de la salud para optimizar el tratamiento y salvar vidas.

Kaggle es una plataforma global dedicada a la ciencia de datos que reúne a una comunidad diversa de expertos, ingenieros y entusiastas para abordar problemas complejos. Utilizando inteligencia artificial y aprendizaje automático, Kaggle fomenta la innovación y el desarrollo de soluciones efectivas para desafíos globales como este.

## Objetivo del Proyecto

El objetivo principal de este proyecto es desarrollar un modelo de aprendizaje automático capaz de detectar con alta precisión la presencia de neumonía en radiografías de tórax. Además, el modelo deberá identificar las áreas específicas en las que la red neuronal se enfoca para determinar si un paciente da positivo o negativo a neumonía.

## Descripción General del Conjunto de Datos

El **análisis de radiografías de tórax para neumonía** es un procedimiento diagnóstico clave para detectar esta enfermedad pulmonar. Consiste en obtener imágenes de los pulmones mediante rayos X, las cuales permiten identificar signos característicos de neumonía, como opacidades blancas o áreas de consolidación que indican inflamación y acumulación de líquido en los alvéolos pulmonares.

En una radiografía, los pulmones de un paciente sano aparecen oscuros debido a su contenido de aire, mientras que en la neumonía se observan anomalías como patrones opacos focales o difusos, pérdida de nitidez en las estructuras anatómicas, y en casos severos, derrame pleural. Este análisis es esencial para confirmar el diagnóstico clínico, evaluar la severidad de la enfermedad y monitorear la respuesta al tratamiento.

- **Imágenes**: Radiografías de tórax.
- **Etiquetas**: Cada imagen está etiquetada para indicar la presencia o ausencia de neumonía con las etiquetas 'NORMAL' y 'PNEUMONIA'.
- **Formato**: Las imágenes están en formato JPEG, facilitando su manejo y procesamiento.
- **Tamaño**: El conjunto de datos incluye un número significativo de imágenes sin embargo se tiene una sobrerrpresentación de la clase 'PNEUMONIA'.

Este proyecto ofrece la posibilidad de impulsar el desarrollo de tecnologías avanzadas para enfrentar la neumonía, optimizando la eficiencia y la exactitud en su diagnóstico, además de fortalecer el acceso a herramientas médicas innovadoras.
