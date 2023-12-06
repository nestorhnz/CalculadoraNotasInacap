import cv2
import numpy as np

# Estas funciones mejoran legibilidad de la imagen para pytesseract, sin embargo no parece necesario en el estado actual del proyecto

def escalar_a_1080p(ruta):   # Aumenta la resolucion a 1080p 
    # Cargar la imagen
    imagen = cv2.imread(ruta)

    # Obtener la altura y anchura de la captura de pantalla
    alto, ancho = imagen.shape[:2]

    # Verificar si la captura ya está en resolución 1080p
    if alto == 1080 and ancho == 1920:
        return ruta  # Si ya es 1080p, no hace falta escalar

    # Calcular el factor de escala para la resolución deseada (1080p)
    factor_escala = min(1920 / ancho, 1080 / alto)

    # Calcular las nuevas dimensiones escaladas manteniendo la proporción
    nuevo_ancho = int(ancho * factor_escala)
    nuevo_alto = int(alto * factor_escala)

    # Aplicar el redimensionamiento a la resolución 1080p
    captura_escalada = cv2.resize(imagen, (nuevo_ancho, nuevo_alto))

    # Crear un lienzo negro de resolución 1080p
    lienzo_1080p = np.zeros((1080, 1920, 3), dtype=np.uint8)

    # Calcular la posición para centrar la imagen escalada en el lienzo negro
    x_offset = (1920 - nuevo_ancho) // 2
    y_offset = (1080 - nuevo_alto) // 2

    # Insertar la imagen escalada en el lienzo negro
    lienzo_1080p[y_offset:y_offset + nuevo_alto, x_offset:x_offset + nuevo_ancho] = captura_escalada

    # Guardar la imagen recortada
    cv2.imwrite(ruta, lienzo_1080p)

    return lienzo_1080p

def mejorar_imagen(ruta):
    # Cargar la imagen
    imagen = cv2.imread(ruta)

    # Aumentar el tamaño de la imagen
    factor = 1.5
    ancho = int(imagen.shape[1] * factor)
    alto = int(imagen.shape[0] * factor)
    nuevo_tamano = (ancho, alto)
    imagen_agrandada = cv2.resize(imagen, nuevo_tamano)

    # Aplicar filtro de suavizado gaussiano
    imagen_mejorada = cv2.GaussianBlur(imagen_agrandada, (5, 5), 0)

    # Ajustar el contraste
    alpha = 1.5  # Factor de contraste, ajusta según sea necesario
    imagen_ajustada = cv2.convertScaleAbs(imagen_mejorada, alpha=alpha, beta=0)

    # Guardar la imagen mejorada
    ruta_salida = ruta
    cv2.imwrite(ruta_salida, imagen_ajustada)

    return ruta

def convertir_a_png(ruta_imagen):   # Devuelve la ruta de la imagen convertida a png
    # Cargar la imagen
    imagen = cv2.imread(ruta_imagen)
    
    # Chequea que la imagen no se PNG
    extension_del_archivo = ruta_imagen.split('.')[-1]
    if extension_del_archivo == 'png':
        return ruta_imagen

    # Verificar si la imagen se cargó correctamente
    if imagen is None:
        print("No se pudo cargar la imagen")
        return

    # Obtener el nombre de archivo sin la extensión
    nombre_archivo_sin_extension = ruta_imagen.split('.')[0]

    # Guardar la imagen en formato PNG
    ruta_destino = nombre_archivo_sin_extension + '.png'
    cv2.imwrite(ruta_destino, imagen)

    return ruta_destino