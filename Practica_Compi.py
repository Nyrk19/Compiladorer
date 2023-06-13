import tkinter as tk
import re

current_token = 0
tokens =""
# Definición de patrones de expresiones regulares para los símbolos terminales
token_patterns = [
    ('main', r'main'),
    ('(', r'\('),
    (')', r'\)'),
    ('{', r'\{'),
    ('}', r'\}'),
    ('imprimir', r'imprimir'),
    ('TipodeDato', r'int|float'),
    ('Id', r'[a-zA-Z][a-zA-Z0-9]*'),
    ('=', r'='),
    (',', r','),
    ('Numero', r'\d+'),
    ('Cadena', r'"([^"\\]|\\.)*"'),
    ('+', r'\+'),
    ('-', r'-'),
    ('*', r'\*'),
    ('/', r'/'),
    (';', r';')
]

def analisis_lexico(code):
    tokens = []
    position = 0
    code_length = len(code)

    while position < code_length:
        current_char = code[position]

        if current_char.isspace():
            position += 1
            continue

        matched = False

        for token_name, pattern in token_patterns:
            regex = re.compile(pattern)
            match = regex.match(code, position)

            if match:
                value = match.group(0)
                tokens.append((token_name, value))
                position = match.end()
                matched = True
                break

        if not matched:
            invalid_char = code[position]
            raise ValueError('Caracter inválido en la posición {}: {}'.format(position, repr(invalid_char)))

        position += 1

    return tokens

# Verifica si el token actual coincide con el tipo esperado
def match(expected_token):
    global current_token
    if current_token < len(tokens) and tokens[current_token][0] == expected_token:
        current_token += 1
    else:
        raise ValueError('Error de sintaxis. Se esperaba "{}" en la posición {}: {}'.format(
            expected_token, current_token, tokens[current_token] if current_token < len(tokens) else 'EOF'))

# Función para el análisis sintáctico
def analisis_sintactico(tokens):
    global current_token
    # Índice del token actual
    current_token = 0

    # Programa -> int main(){ Declaracion AsigOImprimit}
    if tokens[current_token][0] == 'TipodeDato':
        match('TipodeDato')
    match('main')
    match('(')
    match(')')
    match('{')
    parse_declaracion()
    parse_asigOimpimir()
    match('}')

    # Verifica si se han procesado todos los tokens
    if current_token < len(tokens):
        raise ValueError('ParseError de sintaxis. Token inesperado en la posición {}: {}'.format(
            current_token, tokens[current_token]))

    print('Análisis sintáctico exitoso.')

# Declaracion -> TipodeDato Asignacion | TipodeDato Id ; | ε
def parse_declaracion():
    if tokens[current_token][0] == 'TipodeDato':
        match('TipodeDato')
        if tokens[current_token+1][0] == '=':
            parse_asignacion()
            parse_declaracion()
        else:
            match('Id')
            match(';')
            parse_declaracion()

# AsigOImprimir -> Id Asignacion AsigOImprimir | Imprimir AsigOImprimir | ε
def parse_asigOimpimir():
    if tokens[current_token][0] == 'Id':
        parse_asignacion()
        parse_asigOimpimir()
    elif tokens[current_token][0] == 'imprimir':
        parse_imprimir()
        parse_asigOimpimir()

# Asignacion -> Id = Expresion ; Asignacion | ε
def parse_asignacion():
    if tokens[current_token][0] == 'Id':
        match('Id')
        match('=')
        parse_expresion()
        match(';')
        parse_asignacion()

# Expresion -> Termino Expresion'
def parse_expresion():
    parse_termino()
    parse_expresion_prime()

# Expresion' -> + Termino Expresion' | - Termino Expresion' | ε
def parse_expresion_prime():
    if tokens[current_token][0] == '+':
        match('+')
        parse_termino()
        parse_expresion_prime()
    elif tokens[current_token][0] == '-':
        match('-')
        parse_termino()
        parse_expresion_prime()

# Termino -> Factor Termino'
def parse_termino():
    parse_factor()
    parse_termino_prime()

# Termino' -> * Factor Termino' | / Factor Termino' | ε
def parse_termino_prime():
    if tokens[current_token][0] == '*':
        match('*')
        parse_factor()
        parse_termino_prime()
    elif tokens[current_token][0] == '/':
        match('/')
        parse_factor()
        parse_termino_prime()

# Factor -> Numero | ( Expresion ) | Id
def parse_factor():
    if tokens[current_token][0] == 'Numero':
        match('Numero')
    elif tokens[current_token][0] == '(':
        match('(')
        parse_expresion()
        match(')')
    elif tokens[current_token][0] == 'Id':
        match('Id')
    else:
        raise ValueError('ParseFactorError de sintaxis. Token inesperado en la posición {}: {}'.format(
            current_token, tokens[current_token] if current_token < len(tokens) else 'EOF'))

# Imprimir -> imprimir ( Texto Texto' ) ;
def parse_imprimir():
    match('imprimir')
    match('(')
    parse_texto()
    parse_texto_prime()
    match(')')
    match(';')

# Texto -> Cadena | Id
def parse_texto():
    if tokens[current_token][0] == 'Cadena':
        match('Cadena')
    elif tokens[current_token][0] == 'Id':
        match('Id')
    else:
            print('ParseTextoError de sintaxis. Token inesperado en la posición {}: {}'.format(
            current_token, tokens[current_token] if current_token < len(tokens) else 'EOF'))

# Texto' -> , Cadena Texto' | , Id Texto' | ε
def parse_texto_prime():
    if tokens[current_token][0] == ',':
        match(',')
        if tokens[current_token][0] == 'Cadena':
            match('Cadena')
            parse_texto_prime()
            parse_texto_prime()
        elif tokens[current_token][0] == 'Id':
            match('Id')
            parse_texto_prime()
            parse_texto_prime()

def compilar():
    global tokens
    texto = texto_entry.get("1.0", tk.END)  # Obtenertodo el texto
    texto = re.sub(r'\(', ' ( ', texto)
    texto = re.sub(r'\)', ' ) ', texto)
    texto = re.sub(r'\{', ' { ', texto)
    texto = re.sub(r'\}', ' } ', texto)
    texto = re.sub(r'\;', ' ; ', texto)
    texto = re.sub(r'\+', ' + ', texto)
    texto = re.sub(r'-', ' - ', texto)
    texto = re.sub(r'\*', ' * ', texto)
    texto = re.sub(r'\/', ' / ', texto)
    texto = re.sub(r'\=', ' = ', texto)
    texto = re.sub(r'\,', ' , ', texto)
    mensaje_text.config(state=tk.NORMAL)  # Habilitar la edición del segundo campo de texto
    mensaje_text.delete("1.0", tk.END)  # Borrar el contenido anterior del mensaje
    mensaje_text.insert(tk.END, "Iniciando el analisis...\n")  # Agregar el nuevo mensaje
    mensaje_text.config(state=tk.DISABLED)  # Volver a deshabilitar la edición del segundo campo de texto
    tokens = analisis_lexico(texto)
    analisis_sintactico(tokens)
    mensaje_text.config(state=tk.NORMAL)  # Habilitar la edición del segundo campo de texto
    mensaje_text.insert(tk.END, "Termino el analisis\n")  # Agregar el nuevo mensaje
    mensaje_text.config(state=tk.DISABLED)  # Volver a deshabilitar la edición del segundo campo de texto

def correr():
    mensaje_text.config(state=tk.NORMAL)  # Habilitar la edición del segundo campo de texto
    mensaje_text.insert(tk.END, "Comienza a correr el codigo")  # Agregar el nuevo mensaje
    mensaje_text.config(state=tk.DISABLED)  # Volver a deshabilitar la edición del segundo campo de texto

def click(event):
    event.widget.config(relief=tk.SUNKEN)

def liberar(event):
    event.widget.config(relief=tk.RAISED)

def oscurecer(event):
    color_act = event.widget.cget("bg")
    r, g, b =ventana.winfo_rgb(color_act)
    r = int(r * 0.9)
    g = int(g * 0.9)
    b = int(b * 0.9)
    color_new = '#%02x%02x%02x' % (r, g, b)
    event.widget.config(bg=color_new)

def restaurar(event):
    event.widget.config(bg="#f0f0f0")

# Crear la ventana principal
ventana = tk.Tk()

# Maximizar la ventana
ventana.state('zoomed')
ventana.configure(bg="#666666")
ventana.update()

# Crear un marco para contener el campo de texto
marco = tk.Frame(ventana)
marco.config(bg="#666666")
marco.pack(pady=20)

# Crear el campo de texto con desplazamiento (scrollbar)
texto_scrollbar = tk.Scrollbar(marco)
texto_scrollbar.config(troughcolor="#666666")
texto_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

texto_entry = tk.Text(marco, bg="#333333", fg="white", height=int(ventana.winfo_height()*.031), width=int(ventana.winfo_width()*.12))  # Ajustar el tamaño del campo de texto
texto_entry.pack(pady=(0, 10), ipady=5, ipadx=5, padx=5, anchor="w")  # Ajustar los parámetros para reducir el espacio

# Vincular el desplazamiento del texto con la scrollbar
texto_entry.config(yscrollcommand=texto_scrollbar.set)
texto_scrollbar.config(command=texto_entry.yview)

# Crear un marco para contener el segundo campo de texto y el scrollbar
marco_mensaje = tk.Frame(ventana)
marco_mensaje.config(bg="#666666")
marco_mensaje.pack(pady=20)

# Crear el segundo campo de texto con desplazamiento (scrollbar)
mensaje_scrollbar = tk.Scrollbar(marco_mensaje)
mensaje_scrollbar.config(troughcolor="#666666")
mensaje_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

mensaje_text = tk.Text(marco_mensaje, bg="#333333", fg="white", height=int(ventana.winfo_height()*.02), width=int(ventana.winfo_width()*.12), relief="solid", borderwidth=1)
mensaje_text.pack(side=tk.LEFT, fill=tk.BOTH)

mensaje_scrollbar.config(command=mensaje_text.yview)
mensaje_text.config(yscrollcommand=mensaje_scrollbar.set)

# Deshabilitar la edición del segundo campo de texto
mensaje_text.config(state=tk.DISABLED)

# Crear un marco para contener los botones
marco_botones = tk.Frame(ventana)
marco_botones.config(bg="#666666")
marco_botones.pack(pady=10)

# Crear un botón para guardar el texto
guardar_button = tk.Button(marco_botones, text="Compilar", font=("Arial Rounded MT Bold", 12), command=compilar, relief=tk.RAISED, bd=2)
guardar_button.pack(side=tk.LEFT, padx=5)
guardar_button.bind("<Button-1>", click)
guardar_button.bind("<ButtonRelease-1>", liberar)
guardar_button.bind("<Enter>", oscurecer)
guardar_button.bind("<Leave>", restaurar)

# Crear un botón para correr el código
correr_button = tk.Button(marco_botones, text="Correr", font=("Arial Rounded MT Bold", 12), command=correr, relief=tk.RAISED, bd=2)
correr_button.pack(side=tk.LEFT, padx=5)
correr_button.bind("<Button-1>", click)
correr_button.bind("<ButtonRelease-1>", liberar)
correr_button.bind("<Enter>", oscurecer)
correr_button.bind("<Leave>", restaurar)

# Ejecutar el bucle principal de la ventana
ventana.mainloop()
