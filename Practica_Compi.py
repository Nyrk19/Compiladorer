import tkinter as tk
from tkinter import ttk

def guardar_texto():
    texto = texto_entry.get("1.0", tk.END)  # Obtener todo el texto
    mensaje_text.config(state=tk.NORMAL)  # Habilitar la edición del segundo campo de texto
    mensaje_text.delete("1.0", tk.END)  # Borrar el contenido anterior del mensaje
    mensaje_text.insert(tk.END, texto)  # Agregar el nuevo mensaje
    mensaje_text.config(state=tk.DISABLED)  # Volver a deshabilitar la edición del segundo campo de texto

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

texto_entry = tk.Text(marco, height=int(ventana.winfo_height()*.031), width=int(ventana.winfo_width()*.12))  # Ajustar el tamaño del campo de texto
texto_entry.pack(pady=(0, 10), ipady=5, ipadx=5, padx=5, anchor="w")  # Ajustar los parámetros para reducir el espacio

# Vincular el desplazamiento del texto con la scrollbar
texto_entry.config(yscrollcommand=texto_scrollbar.set)
texto_scrollbar.config(command=texto_entry.yview)

# Crear un marco para contener el segundo campo de texto y el scrollbar
marco_mensaje = tk.Frame(ventana)
marco_mensaje.pack(pady=20)

# Crear el segundo campo de texto con desplazamiento (scrollbar)
mensaje_scrollbar = tk.Scrollbar(marco_mensaje)
mensaje_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

mensaje_text = tk.Text(marco_mensaje, height=int(ventana.winfo_height()*.02), width=int(ventana.winfo_width()*.12), relief="solid", borderwidth=1)
mensaje_text.pack(side=tk.LEFT, fill=tk.BOTH)

mensaje_scrollbar.config(command=mensaje_text.yview)
mensaje_text.config(yscrollcommand=mensaje_scrollbar.set)

# Deshabilitar la edición del segundo campo de texto
mensaje_text.config(state=tk.DISABLED)

# Crear un botón para guardar el texto
guardar_button = tk.Button(ventana, text="Compilar", command=guardar_texto)
guardar_button.pack()

# Ejecutar el bucle principal de la ventana
ventana.mainloop()
