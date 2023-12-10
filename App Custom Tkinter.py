import customtkinter as ctk
from Funciones import *
import tkinter as tk

# VARIABLES GLOBALES
ponderaciones_globales = []
calificaciones_globales = []
aprobatoria_global = ''
notas_para_aprobar = {}
modo_actual = "light"

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
            lbl_notas_necesarias.configure(text=f'Para aprobar con {aprobatoria_global} necesitas {notas_para_aprobar}')
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

# Ventana principal
ventana = ctk.CTk()
ventana.geometry('600x450')
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

# Cajas de texto
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
calcular = ctk.CTkButton(vista.tab('Calcular calificaciones'), command=calcular_calificaciones_manualmente, text='Calcular calificaciones')

# Ubicar boton
calcular.grid(row=1, column=4, sticky='w')

# switch modo
switch_var = ctk.StringVar(value="off")
modo_light = ctk.CTkSwitch(vista.tab('Calcular calificaciones'), text="Modo", command=cambiar_modo, variable=switch_var, onvalue="on", offvalue="off")

# Ubicando el switch
modo_light.grid(row=0, column=5, sticky='w')

ventana.mainloop()

