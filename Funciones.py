from PIL import Image                   
from pytesseract import pytesseract     
from datetime import datetime           
import os
import cv2                             
import numpy as np

# FUNCIONES

def captura_a_texto(ruta_de_imagen, ruta_tesseract=r'C:\Program Files\Tesseract-OCR\tesseract.exe'):   # Convierte imagen a texto
        
    try:
        if not os.path.isfile(ruta_de_imagen):
            raise FileNotFoundError("La imagen no existe en la ruta proporcionada.")

        # Apunta pytesseract.tesseract_cmd a tesseract.exe
        pytesseract.tesseract_cmd = ruta_tesseract

        # Abre la imagen con PIL
        imagen = Image.open(ruta_de_imagen)

        # Extrae el texto de la imagen
        texto = pytesseract.image_to_string(imagen, lang='spa')

        # Separa los elementos del texto para almacenarlos en una lista
        lista = texto.split()

        return lista
    except Exception as error:
        print(f'Error: {error}')
        pass

def es_porcentaje(elemento):    # Chequea que el elemento sea un porcentaje
    return elemento[-1] == '%' and elemento[:-1].isdigit()

def es_fecha(elemento):         # Chequea que el elemento sea una fecha 
    formatos_fecha = ['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d'] # En INACAP el formato esperado para fecha es 'dia-mes-año' o '%d-%m-%Y'
    for formato in formatos_fecha:
        try:
            datetime.strptime(elemento, formato)
            return True
        except ValueError:  # Maneja los errores producidos al aplicar el formato a un elemento de la lista que no cumple los requisitos
            pass
    return False

def es_decimal(elemento):       # Chequea que el elemento sea un numero decimal
    try:
        float(elemento)
        return True
    except ValueError:
        return False

def texto_a_numero(elemento, decimal=True):     # Convierte texto a numero
    if decimal == True:
        elemento = float(elemento)
    else:
        elemento = int(elemento)

    return elemento

def ordenar_diccionario(diccionario: dict, llave=True):   # Ordena diccionario de menor a mayor por su llave o su valor

    if llave:
        # Ordenar el diccionario por sus valores en orden ascendente
        diccionario_ordenado = {k: v for k, v in sorted(diccionario.items(), key=lambda item: item[0])}
    else:
        # Ordenar el diccionario por sus valores en orden ascendente
        diccionario_ordenado = {k: v for k, v in sorted(diccionario.items(), key=lambda item: item[1])}

    return diccionario_ordenado

def calcular_calificaciones(porcentajes, calificaciones, calificacion_aprobatoria):    # Calcula las notas necesarias para aprobar

    # DECLARANDO VARIABLES LISTAS Y DICCIONARIOS
    numero_calificaciones_restantes = len(porcentajes) - len(calificaciones)
    porcentaje_aprobacion = (calificacion_aprobatoria * 100) / 7 # EJ: 5.6 = 80 Ese es el porcentaje total necesario para aprobar
    notas_porcentaje = []   # Guarda el valor porcentual final de cada calificacion. EJ: 5.6 en una nota de 25% guardara el valor de 20
    porcentajes_faltantes = {}  # Porcentajes de las evaluaciones que no se han entregado junto con el numero de evaluacion

    # AGREGANDO DATOS A LAS LISTAS Y DICCIONARIOS
    for indice, nota in enumerate(calificaciones):  
        conversion = (nota * porcentajes[indice]) / 7   # Convierte las calificaciones en porcentajes finales usando regla de 3
        notas_porcentaje.append(conversion)

    for i in range(numero_calificaciones_restantes):
        porcentajes_faltantes[4 - i] = porcentajes[-1*(i+1)]    # {Numero de evaluacion:Porcentaje}

    porcentajes_faltantes = ordenar_diccionario(porcentajes_faltantes, llave= False) # Ordena los porcentajes de menor a mayor
    porcentaje_notas_sumadas = sum(notas_porcentaje)

    # 'diferencia' nos permite determinar si el alumno ya aprobo la asignatura
    # Convierte las calificaciones del alumno en la calificacion final independientemente si faltan o no evaluaciones
    diferencia = calificacion_aprobatoria - (sum(notas_porcentaje) * 7 / 100)

    
    if diferencia >= 0: # Las notas del estudiante todavia no son suficientes para haber aprobado la asignatura
       
        suma_porcentajes_restantes = sum(porcentajes_faltantes.values()) 
        
        if (porcentaje_notas_sumadas + suma_porcentajes_restantes) < porcentaje_aprobacion: # Si se cumple, reprobo la asignatura
            return False 
        else:   
            # CALCULO DE CALIFICACIONES NECESARIAS PARA APROBAR

            # Porcentaje necesario que necesita conseguir el alumno para aprobar 
            porcentaje_necesario = porcentaje_aprobacion - porcentaje_notas_sumadas 

            # Porcentaje distribuido equitativamente en el numero de evaluaciones restantes
            porcentaje_individual = porcentaje_necesario / numero_calificaciones_restantes 

            # Almacenara las calificaciones necesarias para aprobar
            notas_necesarias = {}

            # Si un porcentaje individual es mayor al valor de la evaluacion, exceso guardara el porcentaje excedente
            exceso = 0

            # Añadiendo las calificaciones necesarias para aprobar
            for numero_evaluacion, porcentaje in porcentajes_faltantes.items():
                if porcentaje_individual > porcentaje:
                    notas_necesarias[f'Evaluacion {numero_evaluacion}'] = 7 
                    exceso += porcentaje_individual - porcentaje
                else:
                    porcentaje_mas_exceso = porcentaje_individual + exceso

                    if porcentaje_mas_exceso < porcentaje:
                        calificacion_aprobatoria = (porcentaje_mas_exceso * 7) / porcentaje
                        notas_necesarias[f'Evaluacion {numero_evaluacion}'] = calificacion_aprobatoria
                        exceso = 0
                    else:
                        notas_necesarias[f'Evaluacion {numero_evaluacion}'] = 7
                        exceso += porcentaje_individual - porcentaje

            return ordenar_diccionario(notas_necesarias) # No devuelve en orden de las evaluaciones
                    
    else:   # Ya aprobo la asignatura 
        return True 

def calificar_texto(lista: list):   # Califica los elementos del texto obtenido de la captura

    # Listas para almacenar los elementos clasificados
    porcentajes = []
    fechas = []
    calificaciones = []
    otros = []

    # Clasificar los elementos en las listas correspondientes
    for elemento in lista:
        if es_porcentaje(elemento):
            numero = elemento[:-1]
            porcentajes.append(texto_a_numero(numero, decimal=False))
        elif es_fecha(elemento):
            fechas.append(elemento)
        elif es_decimal(elemento):
            if texto_a_numero(elemento) > 7:
                elemento = texto_a_numero(elemento) / 10
                
            calificaciones.append(texto_a_numero(elemento))
        else:
            otros.append(elemento)

    return porcentajes, fechas, calificaciones, otros

def buscar_coincidencia(imagen_completa: str, imagen_a_buscar: str):  # Busca una imagen dentro de otra
    pantalla_completa_img = cv2.imread(imagen_completa, cv2.IMREAD_UNCHANGED)
    nota_img = cv2.imread(imagen_a_buscar, cv2.IMREAD_UNCHANGED)

    result = cv2.matchTemplate(pantalla_completa_img, nota_img, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    w = nota_img.shape[1]
    h = nota_img.shape[0]

    cv2.rectangle(pantalla_completa_img, max_loc, (max_loc[0] + w, max_loc[1] + h), (0,255,255), 2)

    threshold = 0.78

    # Filtrando los resultados
    yloc, xloc = np.where(result >= threshold)

    for (x, y) in zip(xloc, yloc):
        cv2.rectangle(pantalla_completa_img, (x, y), (x + w, y + h), (0,255,255), 2)

    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    # Agrupar los rectangulos
    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

    # Obtener las coordenadas de la imagen dentro de la captura
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    # Recortar la región de interés de la imagen completa
    area_interes = pantalla_completa_img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

    # Extraer el directorio padre de la ruta de la imagen
    directorio = os.path.dirname(imagen_completa)

    # Guardar la imagen recortada
    cv2.imwrite(directorio+'/Coincidencia.png', area_interes)

    # Guardamos la ruta
    coincidencia = directorio+'/Coincidencia.png'

    return  coincidencia


# # Ejemplo de como funciona:

# pantalla_completa = 'C:/Imagenes/BD3.png'                                             # Ruta de captura de pantalla completa
# imagen_ponderaciones = 'C:/Imagenes/Ponderacion titulo.png'                           # Imagen de referencia 1
# imagen_calificaciones = 'C:/Imagenes/Nota.png'                                        # Imagen de referencia 2

# coincidencia_nota = buscar_coincidencia(pantalla_completa, imagen_calificaciones)     # Buscamos coincidencias 
# texto_notas = captura_a_texto(coincidencia_nota)                                      # Extraemos el texto de las coincidencias
# _, _, calificaciones, _ = calificar_texto(texto_notas)                                # Guardamos el texto despues de calificarlo

# coincidencia_ponderaciones = buscar_coincidencia(pantalla_completa, imagen_ponderaciones)
# texto_ponderaciones = captura_a_texto(coincidencia_ponderaciones)
# ponderaciones, _, _, _ = calificar_texto(texto_ponderaciones)



# for i in range(len(ponderaciones)):
#         if i + 1 <= len(calificaciones):
#             print(f'La evaluacion #{i+1} tiene una ponderacion del {ponderaciones[i]}% y el alumno saco un: {calificaciones[i]}')
#         else:
#             print(f'La evaluacion #{i+1} tiene una ponderacion del {ponderaciones[i]}% y el alumno todavia no ha presentado la evaluacion')
# print('')                             

# nota_necesaria = 5
# notas_aprobatorias = calcular_calificaciones(ponderaciones, calificaciones, nota_necesaria)   
# for llave, valor in notas_aprobatorias.items():
#     print(f'Para probar con {nota_necesaria} necesitas aprobar la {llave} con un {valor}')


# Chequear el documento READ ME

