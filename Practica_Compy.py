import tkinter as tk

def guardar_texto():
    texto = texto_entry.get("1.0", tk.END)  # Obtenertodo el texto
    print(texto)

# Crear la ventana principal
ventana = tk.Tk()

# Maximizar la ventana
ventana.state('zoomed')
ventana.update()

# Crear un marco para contener el campo de texto
marco = tk.Frame(ventana)
marco.pack(pady=20)

# Crear el campo de texto con desplazamiento (scrollbar)
texto_scrollbar = tk.Scrollbar(marco)
texto_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

texto_entry = tk.Text(marco, height=int(ventana.winfo_height()*.055), width=int(ventana.winfo_width()*.12))  # Ajustar el tamaño del campo de texto
texto_entry.pack(pady=(0, 10), ipady=5, ipadx=5, padx=5, anchor="w")  # Ajustar los parámetros para reducir el espacio

# Vincular el desplazamiento del texto con la scrollbar
texto_entry.config(yscrollcommand=texto_scrollbar.set)
texto_scrollbar.config(command=texto_entry.yview)

# Crear un botón para guardar el texto
guardar_button = tk.Button(ventana, text="Compilar", command=guardar_texto)
guardar_button.pack()

# Ejecutar el bucle principal de la ventana
ventana.mainloop()
