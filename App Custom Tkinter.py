import customtkinter as ctk
from Funciones import *

# Ventana principal
ventana = ctk.CTk()
ventana.geometry('600x500')
ventana.title('Nota +')

# Marco principal
marco = ctk.CTkFrame(ventana, fg_color='transparent', width=580, height=480)
marco.grid(row=0,column=0)

# Marco de la notas
marco_notas = ctk.CTkFrame(marco, fg_color='transparent')
marco_notas.grid(row=0,column=0, padx=20, pady=20)

# Etiquetas de las notas
lbl_calificaciones = ctk.CTkLabel(master=marco_notas, text='Calificación')
lbl_ponderaciones = ctk.CTkLabel(master=marco_notas, text='Ponderación')

# Ubicando las etiquetas
lbl_calificaciones.grid(row=0, column=0)
lbl_ponderaciones.grid(row=0, column=1)

# Cajas de texto
nota_1 = ctk.CTkEntry(marco_notas, width=60, placeholder_text='Nota 1')
nota_2 = ctk.CTkEntry(marco_notas, width=60, placeholder_text='Nota 2')
nota_3 = ctk.CTkEntry(marco_notas, width=60, placeholder_text='Nota 3')
nota_4 = ctk.CTkEntry(marco_notas, width=60, placeholder_text='Nota 4')
ponderacion_1 = ctk.CTkEntry(marco_notas, width=60, placeholder_text='EJ: 25%')
ponderacion_2 = ctk.CTkEntry(marco_notas, width=60, placeholder_text='EJ: 25%')
ponderacion_3 = ctk.CTkEntry(marco_notas, width=60, placeholder_text='EJ: 25%')
ponderacion_4 = ctk.CTkEntry(marco_notas, width=60, placeholder_text='EJ: 25%')

# Ubicando cajas de texto
nota_1.grid(row=1, column=0, padx=10, pady=10)
nota_2.grid(row=2, column=0, padx=10, pady=10)
nota_3.grid(row=3, column=0, padx=10, pady=10)
nota_4.grid(row=4, column=0, padx=10, pady=10)
ponderacion_1.grid(row=1, column=1, padx=10)
ponderacion_2.grid(row=2, column=1, padx=10)
ponderacion_3.grid(row=3, column=1, padx=10)
ponderacion_4.grid(row=4, column=1, padx=10)


# Check box









ventana.mainloop()








