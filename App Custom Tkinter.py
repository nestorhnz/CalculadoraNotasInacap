import customtkinter as ctk
from Funciones import *
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk
import os
import shutil
from CTkToolTip import *
from tkinter import PhotoImage

import matplotlib.pyplot as plt

# VARIABLES
ponderaciones_globales = []
calificaciones_globales = []
aprobatoria_global = ''
notas_para_aprobar = {}
modo_actual = "light"
ruta_notas = ''
ruta_ponderaciones = ''
ruta_pantalla = ''
ponderaciones_faltantes_globales = []

# FUNCIONES
def obtener_ponderaciones():    # Obtiene las ponderaciones, las convierte a int y guarda en ponderaciones_globales
    global ponderaciones_globales

    # cp = Caja ponderacion 
    cp1 = ponderacion_1.get()
    cp2 = ponderacion_2.get()
    cp3 = ponderacion_3.get()
    cp4 = ponderacion_4.get()

    # Manejo de errores
    try:
        if cp1 == '' or cp2 == '' or cp3 == '' or cp4 == '':    # Chequea si alguna ponderacion no ha sido ingresada
            raise EntryVacio
        p1 = int(cp1)
        p2 = int(cp2)
        p3 = int(cp3)
        p4 = int(cp4)
        if p1 + p2 + p3 + p4 == 100 and p1 * p2 * p3 * p4 != 0:
            ponderaciones_globales = [p1, p2, p3, p4]
            return True
        else:
            raise PonderacionMenorA100
    except ValueError:
        lbl_alerta.configure(text=f'Por favor ingresa solamente numeros enteros en las ponderaciones')
    except EntryVacio:
        lbl_alerta.configure(text='Faltan ponderaciones por ingresar')
    except PonderacionMenorA100:
        lbl_alerta.configure(text='Las ponderaciones deben sumar a 100 y no puede haber ninguna en 0')
    except Exception as err:
        lbl_alerta.configure(text=f'Ha ocurrido un error {err}')
    return

def obtener_calificaciones():   # Obtiene las calificaciones, las convierte a float y guarda en calificaciones_globales
    global calificaciones_globales

    # cc = Caja de calificaciones
    cc1 = nota_1.get()
    cc2 = nota_2.get()
    cc3 = nota_3.get()
    cc4 = nota_4.get()

    lista = [cc1, cc2, cc3, cc4]
    lista_sin_vacios = [elemento for elemento in lista if elemento != '']    # Quitando las notas donde no se ingreso nada
    calificaciones = []     # Calificaciones convertidas a decimal

    try:
        if len(lista_sin_vacios) == 0:
            lbl_alerta.configure(text='No hay ninguna calificación ingresada')
            return
        for elemento in lista_sin_vacios:
            calificaciones.append(float(elemento))
        for calificacion in calificaciones:
            if calificacion > 7 or calificacion < 1:
                raise MalaCalificacion
        calificaciones_globales = calificaciones[:]
        return True
    except ValueError:
        lbl_alerta.configure(text=f'Por favor ingresa solamente numeros en la seccion de notas')
    except MalaCalificacion:
        lbl_alerta.configure(text=f'La calificación ingresada es muy alta o muy baja, ingresa numeros entre 1.0 y 7.0')
    except Exception as err:
        lbl_alerta.configure(text=f'Ha ocurrido un error {err}')
    return

def obtener_calificacion_aprobatoria(): # Obtiene la calificacion aprobatoria y la guarda
    global aprobatoria_global
    # cca = Caja calificacion aprobatoria
    cca = nota_aprobatoria.get()

    try:
        if cca == '':
            raise TypeError
        else:
            nota = float(cca)
            if nota > 7 or nota < 1:
                raise MalaCalificacion
            else:
                aprobatoria_global = nota
                return True
    except TypeError:
        lbl_alerta.configure(text='La nota aprobatoria no puede estar vacia')
    except ValueError:
        lbl_alerta.configure(text=f'La nota aprobatoria debe ser un número')
    except MalaCalificacion:
        lbl_alerta.configure(text=f'La calificación ingresada es muy alta o muy baja, ingresa numeros entre 1.0 y 7.0')
    return

def obtener_todo():  # Obtiene todos los valores de las cajas de texto
    obtener_ponderaciones()
    obtener_calificaciones()
    obtener_calificacion_aprobatoria()
    return

def calcular_calificaciones_manualmente():  # Calcula las calificaciones que has sido ingresadas manualmente
    global notas_para_aprobar, ponderaciones_faltantes_globales

    obtener_todo()
    if ponderaciones_globales and calificaciones_globales and aprobatoria_global:

        # Borrar y reescriben las cajas de texto con el fin de eliminar calculos anteriores
        borrar_caja_texto()
        escribir_entry(ponderaciones_globales, 1)
        escribir_entry(calificaciones_globales, 2)
        
        # Guarda los porcentajes de las evaluaciones que no tienen calificacion
        ponderaciones_faltantes_globales = [elemento for elemento in ponderaciones_globales[(len(calificaciones_globales)-len(ponderaciones_globales)):]]

        notas_para_aprobar = calcular_calificaciones(ponderaciones_globales, calificaciones_globales, aprobatoria_global)
        nota_actual = nota_final_actual(ponderaciones_globales, calificaciones_globales)
        lbl_alerta.configure(text='Campos ingresados correctamente')
        lbl_nota_total.configure(text=f'Tu calificación final con las notas que tienes hasta el momento es {nota_actual}')
        if notas_para_aprobar == True:
            lbl_notas_necesarias.configure(text='¡Felicidades! Tus calificaciones actuales son suficientes para aprobar')
        elif notas_para_aprobar == False:
            lbl_notas_necesarias.configure(text=f'Lamentablemente tus calificaciones no son suficientes para aprobar...')
        else:
            imprimir_nota = ''
            for llave, valor in notas_para_aprobar.items():
                imprimir_nota += f'Un {valor} en la {llave}\n'
            lbl_notas_necesarias.configure(text=f'Para aprobar con {aprobatoria_global} necesitas:')
            lbl_evaluaciones.configure(text=imprimir_nota)
        
        btn_proyeccion = ctk.CTkButton(vista.tab('Calcular calificaciones'), command=mostrar_grafico, text='Mostrar grafico')
        btn_proyeccion.grid(row=4, column=4, sticky='w')
    return

def nota_final_actual(ponderaciones: list, calificaciones: list):   # Calcula la nota actual del estudiante (Nota final)
    # LISTA
    notas_porcentaje = []   # Guarda el valor porcentual final de cada calificacion. EJ: 5.6 en una nota de 25% guardara el valor de 20
    # AGREGANDO DATOS A LA LISTA
    for indice, nota in enumerate(calificaciones):  
        conversion = (nota * ponderaciones[indice]) / 7   # Convierte las calificaciones en ponderaciones finales usando regla de 3
        notas_porcentaje.append(conversion)
    # Convierte las calificaciones del alumno en la calificacion final independientemente si faltan o no evaluaciones
    final = round((sum(notas_porcentaje) * 7 / 100),1)
    return final
        
def cambiar_modo(): # Cambia de modo obscuro a claro y viceversa
    global modo_actual
    if modo_actual == "light":
        ctk.set_appearance_mode("dark")
        modo_actual = "dark"
    else:
        ctk.set_appearance_mode("light")
        modo_actual = "light"

def cargar_img(numero): # Ingresa la ruta de la imagen cargada a las variables ruta_notas, ruta_ponderaciones y ruta_pantalla
    global ruta_notas, ruta_ponderaciones, ruta_pantalla
    extensiones_imagen = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    contador = 0
    if numero == 1:
        try:
            ruta_notas = filedialog.askopenfilename()

            for ext in extensiones_imagen:
                if ruta_notas.lower().endswith(ext):
                    contador += 1
            if contador == 1:
                imagen_comprobar(0)
                contador = 0
        except Exception as e:
            lbl_alerta_2.configure(text=f'Ha ocurrido un error, intenta nuevamente')
        return 
    elif numero == 2:
        try:
            ruta_ponderaciones = filedialog.askopenfilename()
            for ext in extensiones_imagen:
                if ruta_ponderaciones.lower().endswith(ext):
                    contador += 1
            if contador == 1:
                imagen_comprobar(1)
                contador = 0    
        except Exception as e:
            lbl_alerta_2.configure(text=f'Ha ocurrido un error, intenta nuevamente')
        return
    elif numero == 3:
        try:
            ruta_pantalla = filedialog.askopenfilename()
            for ext in extensiones_imagen:
                if ruta_pantalla.lower().endswith(ext):
                    contador += 1
            if contador == 1:
                imagen_comprobar(2)
                contador = 0
        except Exception as e:
            lbl_alerta_2.configure(text=f'Ha ocurrido un error, intenta nuevamente')
        return
    return

def copiar_imagen(ruta_original):   # Copia las imagenes cargadas en la ruta donde se encuentra main
    # Directorio actual
    directorio_actual = os.getcwd()

    # Obtiene el nombre de la imagen con su extension
    nombre_imagen = os.path.basename(ruta_original)

    # Ruta destino (directorio actual)
    ruta_destino = os.path.join(directorio_actual, nombre_imagen)

    # Copiar la imagen a la carpeta actual
    shutil.copyfile(ruta_original, ruta_destino)

    return

def chequear_rutas(): # Chequea que haya imagenes cargadas en las variables ruta_notas, ruta_ponderaciones y ruta_pantalla
    global ruta_notas, ruta_ponderaciones, ruta_pantalla
    lista_de_rutas = [ruta_notas, ruta_ponderaciones, ruta_pantalla]
    extensiones_imagen = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    contador = 0

    for ruta in lista_de_rutas:
        for ext in extensiones_imagen:
            if ruta.lower().endswith(ext):
                contador += 1
    
    if contador == 3:
        try: 
            copiar_imagen(ruta_notas)
            copiar_imagen(ruta_ponderaciones)
            copiar_imagen(ruta_pantalla)
        except Exception as e:
            lbl_alerta_2.configure(text=f'Ha ocurrido un error, intenta nuevamente. Error: {e}')
    else:
        lbl_alerta_2.configure(text='Faltan imagenes por cargar, o alguno de los archivos no son imagenes validas')
        raise Exception('Error, no hay imagenes cargadas')
    return

def imagen_comprobar(columna):   # Crea un preview de la imagen y la ubica en la vista "Subir imagenes"
    imagen_comprobar = PhotoImage(file='comprobar.png')
    if columna == 0:
        #Ubicando etiqueta
        lbl_calificaciones_1 = ctk.CTkLabel(master=vista.tab('Subir imagenes'), text='¡Imagen lista!', justify='center', anchor='n')
        lbl_calificaciones_1.grid(row=1, column=0, sticky='n')
        
        # Ubicando ejemplos de imagenes
        btn_falso_1 = ctk.CTkButton(master=vista.tab('Subir imagenes'), text='', image= imagen_comprobar, fg_color="transparent", hover=False)
        btn_falso_1.grid(row=1, column=columna, sticky='n', pady = 20)

    if columna == 1:
        #Ubicando etiqueta
        lbl_ponde_1 = ctk.CTkLabel(master=vista.tab('Subir imagenes'), text='¡Imagen lista!', justify='center', anchor='n')
        lbl_ponde_1.grid(row=1, column=1, sticky='n')
        
        # Ubicando ejemplos de imagenes
        btn_falso_2 = ctk.CTkButton(master=vista.tab('Subir imagenes'), text='', image= imagen_comprobar, fg_color="transparent", hover=False)
        btn_falso_2.grid(row=1, column=columna, sticky='n', pady = 20)
    if columna == 2:
        #Ubicando etiqueta
        lbl_captu_1 = ctk.CTkLabel(master=vista.tab('Subir imagenes'), text='¡Imagen lista!', justify='center', anchor='n')
        lbl_captu_1.grid(row=1, column=2, sticky='n')
        
        # Ubicando ejemplos de imagenes
        btn_falso_2 = ctk.CTkButton(master=vista.tab('Subir imagenes'), text='', image= imagen_comprobar, fg_color="transparent", hover=False)
        btn_falso_2.grid(row=1, column=columna, sticky='n', pady = 20)

def llamar_funciones():     # Llama las funciones chequear_ruta, borrar y escribir entry, y cambia de vista
    global ruta_notas, ruta_ponderaciones, ruta_pantalla

    try:
        chequear_rutas() # Chequeamos que esten las imagenes cargadas y las copiamos a la ruta del archivo main
        coincidencia_nota = buscar_coincidencia(ruta_pantalla, ruta_notas)     # Buscamos coincidencias 
        texto_notas = captura_a_texto(coincidencia_nota)                       # Extraemos el texto de las coincidencias
        _, _, calificaciones, _ = calificar_texto(texto_notas)                 # Guardamos el texto despues de clasificarlo

        coincidencia_ponderaciones = buscar_coincidencia(ruta_pantalla, ruta_ponderaciones) # Hacemos lo mismo con las ponderaciones
        texto_ponderaciones = captura_a_texto(coincidencia_ponderaciones)
        ponderaciones, _, _, _ = calificar_texto(texto_ponderaciones)

        nombre_imagen_notas = os.path.basename(ruta_notas)
        nombre_imagen_ponderaciones = os.path.basename(ruta_ponderaciones)
        nombre_imagen_pantalla = os.path.basename(ruta_pantalla)

        eliminar_archivo(nombre_imagen_notas)   # Ahora que ya utilizamos las imagenes podemos eliminarlas
        eliminar_archivo(nombre_imagen_ponderaciones)
        eliminar_archivo(nombre_imagen_pantalla)

        borrar_caja_texto() # Borra texto
        escribir_entry(calificaciones, 2) # Escribe las calificaciones en las cajas de calificaciones
        escribir_entry(ponderaciones, 1)  # Escribe las ponderaciones en las cajas de ponderaciones

        lbl_alerta_2.configure(text='')

        vista.set('Calcular calificaciones')

    except Exception as e:
        lbl_alerta.configure(text=f'Ha ocurrido un error {e}')

def borrar_caja_texto():    # Borra todo el texto escrito en las cajas de notas y ponderaciones
    lista_cajas_texto = [nota_1, nota_2, nota_3, nota_4, ponderacion_1, ponderacion_2, ponderacion_3, ponderacion_4, nota_aprobatoria]
    for caja in lista_cajas_texto:
        caja.delete(0, 'end')  # Borrar todo el contenido de la caja de texto
    
    lbl_alerta.configure(text='')
    lbl_nota_total.configure(text='')
    lbl_notas_necesarias.configure(text='')
    lbl_evaluaciones.configure(text='')
    return
    
def escribir_entry(lista, numero):   # Escribe texto en entry
    cajas_de_ponderaciones = [ponderacion_1, ponderacion_2, ponderacion_3, ponderacion_4]
    cajas_de_notas = [nota_1, nota_2, nota_3, nota_4]

    if numero == 1:
        for caja_p, ponderacion in zip(cajas_de_ponderaciones, lista):
            caja_p.insert(0, ponderacion)  # Insertar el nuevo texto en el Entry
    elif numero == 2:
        for caja_n, nota in zip(cajas_de_notas, lista):
            caja_n.insert(0, nota)  # Insertar el nuevo texto en el Entry
        nota_aprobatoria.insert(0, 3.5)
    return

def eliminar_archivo(ruta_archivo): # Elimina archivo
    try:
        # Elimina el archivo en la ruta proporcionada
        os.remove(ruta_archivo)
    except FileNotFoundError:
        lbl_alerta_2.configure(text=f'No se encontró el archivo')
    except Exception as e:
        lbl_alerta_2.configure(text=f'Ocurrio un error: {e}')
    return

def mostrar_imagen(event, master_1, imagen, x: int, y: int):    # Muestra imagen en tooltip
    global imagen_mostrada, etique1
    imagen_mostrada = tk.PhotoImage(file=imagen)
    etique1 = tk.Label(master=master_1)
    etique1.place(x=x, y=y)
    etique1.config(image=imagen_mostrada)
    return

def ocultar_imagen(event):  # Destruye imagen creada en tooltip
    etique1.destroy()
    return

def estimar_notas(notas:list):   # Hace un promedio de las calificaciones que tiene el estudiante y regresa una lista con estimaciones
    notas_estimadas = []
    for i in range((4-len(notas))):
        notas_estimadas.append(sum(notas)/len(notas))
    return notas_estimadas

# Ventana principal
ventana = ctk.CTk()
ventana.geometry('600x500')
ventana.title('Nota +')

# Creando vistas
vista = ctk.CTkTabview(ventana)
# Ubicando las vistas
vista.pack(pady=20, padx=20, expand = 1)
# Añadiendo vistas
vista.add('Calcular calificaciones')
vista.add('Subir imagenes')
# Vista principal
vista.set('Calcular calificaciones')

################################################### VISTA: CALCULAR CALIFICACIONES ################################################### 

# Etiquetas 
lbl_calificaciones = ctk.CTkLabel(master=vista.tab('Calcular calificaciones'), text='Calificación')
lbl_ponderaciones = ctk.CTkLabel(master=vista.tab('Calcular calificaciones'), text='Ponderación')
lbl_aprobatoria = ctk.CTkLabel(master=vista.tab('Calcular calificaciones'), text='Nota aprobatoria')
lbl_porcen1 = ctk.CTkLabel(master=vista.tab('Calcular calificaciones'), text='%')
lbl_porcen2 = ctk.CTkLabel(master=vista.tab('Calcular calificaciones'), text='%')
lbl_porcen3 = ctk.CTkLabel(master=vista.tab('Calcular calificaciones'), text='%')
lbl_porcen4 = ctk.CTkLabel(master=vista.tab('Calcular calificaciones'), text='%')
lbl_alerta = ctk.CTkLabel(master=vista.tab('Calcular calificaciones'), text='')
lbl_nota_total = ctk.CTkLabel(master=vista.tab('Calcular calificaciones'),text='')
lbl_notas_necesarias = ctk.CTkLabel(master=vista.tab('Calcular calificaciones'),text='')
lbl_evaluaciones = ctk.CTkLabel(master=vista.tab('Calcular calificaciones'),text='')

# Ubicando las etiquetas 
lbl_calificaciones.grid(row=0, column=0, sticky='w')
lbl_ponderaciones.grid(row=0, column=1, sticky='w')
lbl_aprobatoria.grid(row=0, column=3, sticky='w')
lbl_porcen1.grid(row=1, column=2, sticky='w')
lbl_porcen2.grid(row=2, column=2, sticky='w')
lbl_porcen3.grid(row=3, column=2, sticky='w')
lbl_porcen4.grid(row=4, column=2, sticky='w')
lbl_alerta.grid(row=6, column=0, sticky='w', columnspan=5)
lbl_nota_total.grid(row=7, column=0, sticky='w', columnspan=10)
lbl_notas_necesarias.grid(row=8, column=0, sticky='w', columnspan=10)
lbl_evaluaciones.grid(row=9, column=0, sticky='w', columnspan=10, rowspan=10)

# Cajas de texto de 
nota_1 = ctk.CTkEntry(vista.tab('Calcular calificaciones'), width=60, placeholder_text='Nota 1')
nota_2 = ctk.CTkEntry(vista.tab('Calcular calificaciones'), width=60, placeholder_text='Nota 2')
nota_3 = ctk.CTkEntry(vista.tab('Calcular calificaciones'), width=60, placeholder_text='Nota 3')
nota_4 = ctk.CTkEntry(vista.tab('Calcular calificaciones'), width=60, placeholder_text='Nota 4')
ponderacion_1 = ctk.CTkEntry(vista.tab('Calcular calificaciones'), width=60, placeholder_text='25')
ponderacion_2 = ctk.CTkEntry(vista.tab('Calcular calificaciones'), width=60, placeholder_text='25')
ponderacion_3 = ctk.CTkEntry(vista.tab('Calcular calificaciones'), width=60, placeholder_text='25')
ponderacion_4 = ctk.CTkEntry(vista.tab('Calcular calificaciones'), width=60, placeholder_text='25')
nota_aprobatoria = ctk.CTkEntry(vista.tab('Calcular calificaciones'), width=60, placeholder_text='Nota')

# Ubicando cajas de texto
nota_1.grid(row=1, column=0, padx=10, pady=10, sticky='w')
nota_2.grid(row=2, column=0, padx=10, pady=10, sticky='w')
nota_3.grid(row=3, column=0, padx=10, pady=10, sticky='w')
nota_4.grid(row=4, column=0, padx=10, pady=10, sticky='w')
ponderacion_1.grid(row=1, column=1, padx=10, sticky='w')
ponderacion_2.grid(row=2, column=1, padx=10, sticky='w')
ponderacion_3.grid(row=3, column=1, padx=10, sticky='w')
ponderacion_4.grid(row=4, column=1, padx=10, sticky='w')
nota_aprobatoria.grid(row=1, column=3, padx=10, pady=10, sticky='w')

# Botones
btn_calcular = ctk.CTkButton(vista.tab('Calcular calificaciones'), command=calcular_calificaciones_manualmente, text='Calcular calificaciones')
btn_limpiar = ctk.CTkButton(vista.tab('Calcular calificaciones'), command=borrar_caja_texto, text='Limpiar', width=64)

# Ubicar boton
btn_calcular.grid(row=1, column=4, sticky='w')
btn_limpiar.grid(row=1, column=5, sticky='w', padx=10)

# switch modo
switch_var = ctk.StringVar(value="off")
modo_light = ctk.CTkSwitch(vista.tab('Calcular calificaciones'), text="Modo", command=cambiar_modo, variable=switch_var, onvalue="on", offvalue="off")

# Ubicando el switch
modo_light.grid(row=0, column=5, sticky='w')

################################################### VISTA: SUBIR IMAGENES ################################################### 

# Etiquetas
lbl_calificaciones = ctk.CTkLabel(master=vista.tab('Subir imagenes'), text='Notas', justify='center', anchor='n')
lbl_ponderaciones = ctk.CTkLabel(master=vista.tab('Subir imagenes'), text='Ponderación', justify='center', anchor='n')
lbl_aprobatoria = ctk.CTkLabel(master=vista.tab('Subir imagenes'), text='Pantalla completa', justify='center', anchor='n')
lbl_alerta_2 = ctk.CTkLabel(master=vista.tab('Subir imagenes'), text='', justify='center', anchor='n')

# Ubicando etiquetas
lbl_calificaciones.grid(row=0, column=0, sticky='n', padx=30, pady=30, rowspan=3)
lbl_ponderaciones.grid(row=0, column=1, sticky='n', padx=30, pady=30, rowspan=3)
lbl_aprobatoria.grid(row=0, column=2, sticky='n', padx=30, pady=30, rowspan=3)
lbl_alerta_2.grid(row=3, column=0, sticky='n', columnspan=3, padx=30, pady=20)

# Modificando el tamaño de las filas y columnas
vista.tab('Subir imagenes').columnconfigure(0, minsize=217)  # Columna 0
vista.tab('Subir imagenes').columnconfigure(1, minsize=210)  # Columna 1
vista.tab('Subir imagenes').columnconfigure(2, minsize=210)  # Columna 2
vista.tab('Subir imagenes').rowconfigure(1, minsize=150)  # Columna 1
vista.tab('Subir imagenes').rowconfigure(3, minsize=40)  # Columna 2

# Imagenes para los botones
imagen_1 = PhotoImage(file='subir(4).png')

# Creando botones para cargar imagenes
btn_cargar_img_1 = ctk.CTkButton(master=vista.tab('Subir imagenes'), text='', command=lambda: cargar_img(1), image= imagen_1, fg_color="transparent", width=64, height=64)
btn_cargar_img_2 = ctk.CTkButton(master=vista.tab('Subir imagenes'), text='', command=lambda: cargar_img(2), image= imagen_1, fg_color="transparent", width=64, height=64)
btn_cargar_img_3 = ctk.CTkButton(master=vista.tab('Subir imagenes'), text='', command=lambda: cargar_img(3), image= imagen_1, fg_color="transparent", width=64, height=64)
btn_calcular_2 = ctk.CTkButton(master=vista.tab('Subir imagenes'), text='Calcular', command=llamar_funciones, width=64)

# Ubicando botones
btn_cargar_img_1.grid(row=0, column=0, padx=15, pady=50)
btn_cargar_img_2.grid(row=0, column=1, padx=15, pady=50)
btn_cargar_img_3.grid(row=0, column=2, padx=15, pady=50)
btn_calcular_2.grid(row=2, column=1, sticky='n')

# Mensajes para los tooltips
mensaje_1 ="Sube una captura pequeña de la tabla de tus calificaciones"
mensaje_2 ="Sube una captura pequeña de la tabla de tus ponderaciones"
mensaje_3 ="Sube una captura de pantalla completa"

# Creando tooltips
tooltip_1 = CTkToolTip(btn_cargar_img_1, delay=0, message=mensaje_1, x_offset=+15, y_offset=+5)
tooltip_2 = CTkToolTip(btn_cargar_img_2, delay=0, message=mensaje_2, x_offset=+15, y_offset=+5)
tooltip_3 = CTkToolTip(btn_cargar_img_3, delay=0, message=mensaje_3, x_offset=+15, y_offset=+5)

# Rutas de las imagenes de los tooltips
ruta_ejemplo_1 = 'ejemplo_notas.png'
ruta_ejemplo_2 = 'ejemplo_ponderaciones.png'
ruta_ejemplo_3 = 'ejemplo_pantalla_completa.png'

# Asociar eventos para mostrar y ocultar la imagen al pasar el mouse sobre el botón
btn_cargar_img_1.bind("<Enter>",lambda event: mostrar_imagen(event, vista.tab('Subir imagenes'), ruta_ejemplo_1, 265, 185))
btn_cargar_img_1.bind("<Leave>", ocultar_imagen)

btn_cargar_img_2.bind("<Enter>",lambda event: mostrar_imagen(event, vista.tab('Subir imagenes'), ruta_ejemplo_2, 175, 180))
btn_cargar_img_2.bind("<Leave>", ocultar_imagen)

btn_cargar_img_3.bind("<Enter>",lambda event: mostrar_imagen(event, vista.tab('Subir imagenes'), ruta_ejemplo_3, 120, 180))
btn_cargar_img_3.bind("<Leave>", ocultar_imagen)

################################################### VISTA: PROYECCION DE NOTAS ################################################### 

def mostrar_grafico():
    global notas_para_aprobar

    notas = calificaciones_globales
    ponderaciones = ponderaciones_globales
    faltantes = ponderaciones_faltantes_globales
    evaluaciones = [1,2,3,4]
    x_values = [1,2,3,4,5,6,7]
    y_values = [10,15,20,25,30,35,40] + ponderaciones
    
    # Ajusta la longitud de la lista porque X y Y deben tener el mismo tamaño
    if len(notas) < 4:
        ponderaciones = ponderaciones[:(len(notas))]

    # Si todavia no ha aprobado ni reprobado, se muestran las notas aprobatorias (notas_para_aprobar solo puede ser dict, True o False)
    if type(notas_para_aprobar) == dict:
        grafica_1 = plt.scatter(notas_para_aprobar.values(), faltantes)
        grafica_2 = plt.scatter(estimar_notas(notas), faltantes)

    # Se muestra las calificaciones actuales
    grafica_3 = plt.scatter(notas, ponderaciones)
    plt.title('Progreso del estudiante')
    plt.xlabel('Calificaciones')
    plt.ylabel('Ponderaciones')

    # Nombre de las graficas
    if type(notas_para_aprobar) == dict:
        plt.legend(['Calificaciones necesarias para aprobar','Calificaciones futuras estimadas','Calificaciones actuales'])
        x_values += notas_para_aprobar.values() 
        x_values += estimar_notas(notas)
    else:
        plt.legend(['Calificaciones actuales'])

    plt.xticks(x_values)  
    plt.yticks(y_values)

    plt.show()

ventana.mainloop()