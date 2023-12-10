import customtkinter as ctk
from Funciones import *
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk
import os
import shutil

# VARIABLES
ponderaciones_globales = []
calificaciones_globales = []
aprobatoria_global = ''
notas_para_aprobar = {}
modo_actual = "light"
ruta_notas = ''
ruta_ponderaciones = ''
ruta_pantalla = ''

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
    global notas_para_aprobar

    obtener_todo()
    if ponderaciones_globales and calificaciones_globales and aprobatoria_global:
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
    return

def nota_final_actual(ponderaciones: list, calificaciones: list):   # Calcula la nota actual del estudiante (Nota final)
    # LISTA
    notas_porcentaje = []   # Guarda el valor porcentual final de cada calificacion. EJ: 5.6 en una nota de 25% guardara el valor de 20
    # AGREGANDO DATOS A LA LISTA
    for indice, nota in enumerate(calificaciones):  
        conversion = (nota * ponderaciones[indice]) / 7   # Convierte las calificaciones en ponderaciones finales usando regla de 3
        notas_porcentaje.append(conversion)
    # Convierte las calificaciones del alumno en la calificacion final independientemente si faltan o no evaluaciones
    final = (sum(notas_porcentaje) * 7 / 100)
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
    if numero == 1:
        try:
            ruta_notas = filedialog.askopenfilename()
            lbl_calificaciones_1 = ctk.CTkLabel(master=vista.tab('Subir imagenes'), text='Tus notas', justify='center', anchor='n')
            lbl_calificaciones_1.grid(row=2, column=0, sticky='w', padx=20)
            preview_imagen(ruta_notas, 0)
        except Exception as e:
            lbl_alerta_2.configure(text=f'Ha ocurrido un error, intenta nuevamente')
        return 
    elif numero == 2:
        try:
            ruta_ponderaciones = filedialog.askopenfilename()
            lbl_ponde_1 = ctk.CTkLabel(master=vista.tab('Subir imagenes'), text='Tus ponderaciones', justify='center', anchor='n')
            lbl_ponde_1.grid(row=2, column=1, sticky='w', padx=20)
            preview_imagen(ruta_ponderaciones, 1)
        except Exception as e:
            lbl_alerta_2.configure(text=f'Ha ocurrido un error, intenta nuevamente')
        return
    elif numero == 3:
        try:
            ruta_pantalla = filedialog.askopenfilename()
            lbl_captu_1 = ctk.CTkLabel(master=vista.tab('Subir imagenes'), text='Tu captura', justify='center', anchor='n')
            lbl_captu_1.grid(row=2, column=2, sticky='w', padx=20)
            preview_imagen(ruta_pantalla, 2)
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

def preview_imagen(ruta, columna):   # Crea un preview de la imagen y la ubica en la vista "Subir imagenes"
    if columna == 0:
        # Abrir y redimensionar ejemplos de imagenes
        img1 = Image.open(ruta)
        img1.thumbnail((100, 100))
        img_tk1 = ImageTk.PhotoImage(img1)

        # Ubicando ejemplos de imagenes
        lbl_img1 = tk.Label(master=vista.tab('Subir imagenes'), image=img_tk1)
        lbl_img1.image = img_tk1  # Mantener referencia para evitar que la imagen sea eliminada por el recolector de basura
        lbl_img1.grid(row=2, column=columna, sticky='w', columnspan=3, padx=30, rowspan= 2, pady=50)
    if columna == 1:
        # Abrir y redimensionar ejemplos de imagenes
        img2 = Image.open(ruta)
        img2.thumbnail((100, 100))
        img_tk2 = ImageTk.PhotoImage(img2)

        # Ubicando ejemplos de imagenes
        lbl_img2 = tk.Label(master=vista.tab('Subir imagenes'), image=img_tk2)
        lbl_img2.image = img_tk2  # Mantener referencia para evitar que la imagen sea eliminada por el recolector de basura
        lbl_img2.grid(row=2, column=columna, sticky='w', columnspan=3, padx=30, rowspan= 2, pady=50)
    if columna == 2:
        # Abrir y redimensionar ejemplos de imagenes
        img3 = Image.open(ruta)
        img3.thumbnail((150, 150))
        img_tk3 = ImageTk.PhotoImage(img3)

        # Ubicando ejemplos de imagenes
        lbl_img3 = tk.Label(master=vista.tab('Subir imagenes'), image=img_tk3)
        lbl_img3.image = img_tk3  # Mantener referencia para evitar que la imagen sea eliminada por el recolector de basura
        lbl_img3.grid(row=2, column=columna, sticky='w', columnspan=3, padx=30, rowspan= 2, pady=50)

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

        vista.set('Calcular calificaciones')

    except Exception as e:
        print(f'Ha ocurrido un error, nombre {e}')

def borrar_caja_texto():    # Borra todo el texto escrito en las cajas de notas y ponderaciones
    lista_cajas_texto = [nota_1, nota_2, nota_3, nota_4, ponderacion_1, ponderacion_2, ponderacion_3, ponderacion_4, nota_aprobatoria]
    for caja in lista_cajas_texto:
        caja.delete(0, 'end')  # Borrar todo el contenido de la caja de texto
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

def eliminar_archivo(ruta_archivo):
    try:
        # Elimina el archivo en la ruta proporcionada
        os.remove(ruta_archivo)
    except FileNotFoundError:
        lbl_alerta_2.configure(text=f'No se encontró el archivo')
    except Exception as e:
        lbl_alerta_2.configure(text=f'Ocurrio un error: {e}')
    return

# Ventana principal
ventana = ctk.CTk()
ventana.geometry('600x500')
ventana.title('Nota +')

# Creando vistas
vista = ctk.CTkTabview(ventana)
# Ubicando las vistas
vista.pack(pady=20, padx=20)
# Añadiendo vistas
vista.add('Calcular calificaciones')
vista.add('Subir imagenes')
vista.add('Proyección de notas')
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

# Ubicar boton
btn_calcular.grid(row=1, column=4, sticky='w')

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
lbl_calificaciones.grid(row=0, column=0, sticky='w', padx=30)
lbl_ponderaciones.grid(row=0, column=1, sticky='w', columnspan=3, padx=30)
lbl_aprobatoria.grid(row=0, column=2, sticky='w', columnspan=3, padx=30)
lbl_alerta_2.grid(row=5, column=0, sticky='w', columnspan=3, padx=30)

# Modificando el tamaño de las filas y columnas
vista.tab('Subir imagenes').columnconfigure(0, minsize=217)  # Columna 0
vista.tab('Subir imagenes').columnconfigure(1, minsize=210)  # Columna 1
vista.tab('Subir imagenes').columnconfigure(2, minsize=210)  # Columna 2
vista.tab('Subir imagenes').rowconfigure(0, minsize=84)  # Columna 0
vista.tab('Subir imagenes').rowconfigure(1, minsize=84)  # Columna 1
vista.tab('Subir imagenes').rowconfigure(2, minsize=84)  # Columna 2
vista.tab('Subir imagenes').rowconfigure(3, minsize=84)  # Columna 2
vista.tab('Subir imagenes').rowconfigure(4, minsize=84)  # Columna 2

# Cargando ejemplos de imagenes
ruta_imagen1 = 'Nota2312.png'
ruta_imagen2 = 'p2312.png'
ruta_imagen3 = 'bd2312.png'

# Abrir y redimensionar ejemplos de imagenes
imagen1 = Image.open(ruta_imagen1)
imagen1.thumbnail((100, 100))
imagen_tk1 = ImageTk.PhotoImage(imagen1)

imagen2 = Image.open(ruta_imagen2)
imagen2.thumbnail((100, 100))
imagen_tk2 = ImageTk.PhotoImage(imagen2)

imagen3 = Image.open(ruta_imagen3)
imagen3.thumbnail((150, 150))
imagen_tk3 = ImageTk.PhotoImage(imagen3)

# Ubicando ejemplos de imagenes
label_imagen1 = tk.Label(master=vista.tab('Subir imagenes'), image=imagen_tk1)
label_imagen1.image = imagen_tk1  # Mantener referencia para evitar que la imagen sea eliminada por el recolector de basura
label_imagen1.grid(row=0, column=0, sticky='w', columnspan=3, padx=30, rowspan= 2, pady=50)

label_imagen2 = tk.Label(master=vista.tab('Subir imagenes'), image=imagen_tk2)
label_imagen2.image = imagen_tk2
label_imagen2.grid(row=0, column=1, sticky='w', columnspan=3, padx=30, rowspan= 2, pady=30)

label_imagen3 = tk.Label(master=vista.tab('Subir imagenes'), image=imagen_tk3)
label_imagen3.image = imagen_tk3
label_imagen3.grid(row=0, column=2, sticky='w', columnspan=3, padx=30, rowspan= 2, pady=30)

# Creando botones para cargar imagenes
btn_cargar_img_1 = ctk.CTkButton(master=vista.tab('Subir imagenes'), text='Cargar imagen', command=lambda: cargar_img(1))
btn_cargar_img_2 = ctk.CTkButton(master=vista.tab('Subir imagenes'), text='Cargar imagen', command=lambda: cargar_img(2))
btn_cargar_img_3 = ctk.CTkButton(master=vista.tab('Subir imagenes'), text='Cargar imagen', command=lambda: cargar_img(3))
btn_calcular_2 = ctk.CTkButton(master=vista.tab('Subir imagenes'), text='Calcular', command=llamar_funciones)

# Ubicando botones
btn_cargar_img_1.grid(row=1, column=0, sticky='w', columnspan=3, padx=15)
btn_cargar_img_2.grid(row=1, column=1, sticky='w', columnspan=3, padx=15)
btn_cargar_img_3.grid(row=1, column=2, sticky='w', columnspan=3, padx=15)
btn_calcular_2.grid(row=4, column=1, sticky='w', columnspan=3)

ventana.mainloop()

