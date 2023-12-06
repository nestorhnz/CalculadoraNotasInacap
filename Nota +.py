from Funciones import *
import tkinter as tk

ventana = tk.Tk()
ventana.geometry("800x600")
ventana.title("Nota +")
ventana.resizable(False, False)

alumnos = ["Francisco Mendoza", "Nestor Hernandez", "Matias Illanes", "Esteban Mendoza"]
ramos = ["Matemáticas", "Base de Datos", "Programación", "Administración"]       

frame_buscador = tk.LabelFrame(ventana, text="Buscar Alumno")
buscador = tk.Entry(frame_buscador)
frame_buscador.pack()
buscador.pack(padx=8, pady=6)

tk.Label(ventana, text="Nota +", font="Helvetica 15 italic").place(x=122, y=14)

frame_principal = tk.LabelFrame(ventana, text="Alumno")
frame_principal.pack(side="left", fill="both", expand=True, padx=8, pady=8)

tk.Label(frame_principal, text="Estudiante: ").grid(row=0, column=0, pady=40, sticky="w")
nombre_estudiante = tk.Label(frame_principal, text="")
nombre_estudiante.place(x=80, y=40)
tk.Label(frame_principal, text="Carrera: ").grid(row=1, column=0, pady=20, sticky="w")
nombre_carrera = tk.Label(frame_principal, text="")
nombre_carrera.place(x=66, y=120)
menu_alumnos = tk.Menu(frame_principal, tearoff=0)
  
ramo = tk.StringVar()
ramo.set("Elegir Ramo")
menu_ramos = tk.OptionMenu(frame_principal, ramo, *ramos)
menu_ramos.place(x=620, y=36)

frame_notas = tk.LabelFrame(frame_principal, text="Notas")
frame_notas.grid(row=2, column=0, padx=12, pady=20)

tk.Label(frame_notas, text="Nota 1: ").grid(row=0, column=0, padx=8, pady=8)
tk.Label(frame_notas, text="Nota 2: ").grid(row=1, column=0, padx=8, pady=8)
tk.Label(frame_notas, text="Nota 3: ").grid(row=2, column=0, padx=8, pady=8)
tk.Label(frame_notas, text="Nota 4: ").grid(row=3, column=0, padx=8, pady=8)

n1 = tk.Entry(frame_notas, width=6)
n1.grid(row=0, column=1, padx=8)
n2 = tk.Entry(frame_notas, width=6)
n2.grid(row=1, column=1, padx=8)
n3 = tk.Entry(frame_notas, width=6)
n3.grid(row=2, column=1, padx=8)
n4 = tk.Entry(frame_notas, width=6)
n4.grid(row=3, column=1, padx=8)

tk.Label(frame_notas, text="%").grid(row=1, column=2, padx=6)
tk.Label(frame_notas, text="%").grid(row=2, column=2, padx=6)
tk.Label(frame_notas, text="%").grid(row=3, column=2, padx=6)
tk.Label(frame_notas, text="%").grid(row=0, column=2, padx=6)

percent_n1 = tk.Entry(frame_notas, width=6).grid(row=0, column=3, padx=8)
percent_n2 = tk.Entry(frame_notas, width=6).grid(row=1, column=3, padx=8)
percent_n3 = tk.Entry(frame_notas, width=6).grid(row=2, column=3, padx=8)
percent_n4 = tk.Entry(frame_notas, width=6).grid(row=3, column=3, padx=8)

btn_guardar_notas = tk.Button(frame_principal, text="Guardar notas").place(x=352, y=200)
btn_calcular = tk.Button(frame_principal, text="Calcular notas").place(x=352, y=260)
btn_graficar = tk.Button(frame_principal, text="Graficar progreso").place(x=344, y=376)

frame_notas_esperadas = tk.LabelFrame(frame_principal, text="Notas esperadas")
frame_notas_esperadas.place(x=600, y=181)

tk.Label(frame_notas_esperadas, text="Nota 1: ").grid(row=0, column=0, padx=8, pady=8)
tk.Label(frame_notas_esperadas, text="Nota 2: ").grid(row=1, column=0, padx=8, pady=8)
tk.Label(frame_notas_esperadas, text="Nota 3: ").grid(row=2, column=0, padx=8, pady=8)
tk.Label(frame_notas_esperadas, text="Nota 4: ").grid(row=3, column=0, padx=8, pady=8)

n1_esp = tk.Label(frame_notas_esperadas, text="", width=6)
n1_esp.grid(row=0, column=1, padx=8)
n2_esp = tk.Label(frame_notas_esperadas, text="", width=6)
n2_esp.grid(row=1, column=1, padx=8)
n3_esp = tk.Label(frame_notas_esperadas, text="", width=6)
n3_esp.grid(row=2, column=1, padx=8)
n4_esp = tk.Label(frame_notas_esperadas, text="", width=6)
n4_esp.grid(row=3, column=1, padx=8)

frame_consejo = tk.LabelFrame(ventana, text="Consejo del dia")
frame_consejo.place(x=80, y=500)
tk.Label(frame_consejo, text="", width=88, height=3).pack(side="left")

def mostrar_info(alumno):
    if alumno == "Francisco Mendoza":
        nombre_estudiante.config(text="Francisco Javier Mendoza Forton")
        nombre_carrera.config(text="Analista Programador")
    elif alumno == "Nestor Hernandez":
        nombre_estudiante.config(text="Néstor Enrique Hernández Sánchez")    
        nombre_carrera.config(text="Analista Programador")
    elif alumno == "Matias Illanes":
        nombre_estudiante.config(text="Matias Gabriel Illanes Águila")
        nombre_carrera.config(text="Diseño de Software")
    elif alumno == "Esteban Mendoza":
        nombre_estudiante.config(text="Esteban Patricio Mendoza Pailahueque")
        nombre_carrera.config(text="Ciberseguridad")

def buscar_alumno(event):
    alum = buscador.get().lower()
    menu_alumnos.delete(0, tk.END)
    for alumno in alumnos:
        if alum in alumno.lower():
            menu_alumnos.add_cascade(label=alumno, command=lambda a=alumno: mostrar_info(a))
    x, y, _, _ = buscador.bbox("insert")
    menu_alumnos.post(buscador.winfo_rootx() + x, buscador.winfo_rooty() + y + buscador.winfo_height())
    buscador.delete(0, tk.END)
    
buscador.bind("<Return>", buscar_alumno)  

ventana.mainloop()