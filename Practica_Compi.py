import tkinter as tk
import re

current_token = 0
error_sintactico = False
tabla=[]

# Definición de patrones de expresiones regulares para los símbolos terminales
token_patterns = [
    ('main', r'main'),
    ('(', r'\('),
    (')', r'\)'),
    ('{', r'\{'),
    ('}', r'\}'),
    ('imprimir', r'imprimir'),
    ('sqrt', r'sqrt'),
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
    error_lexico = False

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
            escribir_tx2(f"Carácter inválido en la posición {position}: {repr(invalid_char)}\n")
            error_lexico = True
            break

        position += 1

    if error_lexico:
        return []
    return tokens

# Verifica si el token actual coincide con el tipo esperado
def match(expected_token):
    global current_token
    if current_token < len(tokens) and tokens[current_token][0] == expected_token:
        current_token += 1
    else:
        escribir_tx2('Error de sintaxis. Se esperaba "{}" en la posición {}: {}\n'.format(
            expected_token, current_token, tokens[current_token] if current_token < len(tokens) else 'EOF'))
        error_sintactico = True

# Función para el análisis sintáctico
def analisis_sintactico(tokens):
    global current_token, error_sintactico
    error_sintactico = False
    # Índice del token actual
    current_token = 0

    # Programa -> int main(){ Declaracion AsigOImprimitOSqrt}
    if tokens[current_token][0] == 'TipodeDato':
        match('TipodeDato')
    match('main')
    match('(')
    match(')')
    match('{')
    parse_declaracion()
    parse_asigOimpimirOsqrt()
    match('}')

    # Verifica si se han procesado todos los tokens
    if current_token < len(tokens):
        escribir_tx2('Error de sintaxis. Token inesperado en la posición {}: {}\n'.format(
            current_token, tokens[current_token]))
        error_sintactico = True

    if not error_sintactico:
        escribir_tx2('Análisis sintáctico exitoso.\n')

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

# AsigOImprimirOSqrt -> Id Asignacion AsigOImprimir | Imprimir AsigOImprimir | ε
def parse_asigOimpimirOsqrt():
    if tokens[current_token][0] == 'Id':
        parse_asignacion()
        parse_asigOimpimirOsqrt()
    elif tokens[current_token][0] == 'imprimir':
        parse_imprimir()
        parse_asigOimpimirOsqrt()
    elif tokens[current_token][0] == 'sqrt':
        parse_sqrt()
        parse_asigOimpimirOsqrt()

# Sqrt -> sqrt(Expresion) | ε
def parse_sqrt():
    if tokens[current_token][0] == 'sqrt':
        match('sqrt')
        match('(')
        parse_expresion()
        match(')')
        match(';')

# Asignacion -> Id = Expresion ; | ε
def parse_asignacion():
    if tokens[current_token][0] == 'Id':
        match('Id')
        match('=')
        parse_expresion()
        match(';')

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
        escribir_tx2('Error de sintaxis. Token inesperado en la posición {}: {}\n'.format(
            current_token, tokens[current_token] if current_token < len(tokens) else 'EOF'))
        error_sintactico = True

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
        escribir_tx2('Error de sintaxis. Token inesperado en la posición {}: {}\n'.format(
            current_token, tokens[current_token] if current_token < len(tokens) else 'EOF'))
        error_sintactico = True

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

def escribir_tx2(Text):
    mensaje_text.config(state=tk.NORMAL)  # Habilitar la edición del segundo campo de texto
    mensaje_text.insert(tk.END, Text)  # Agregar el nuevo mensaje
    mensaje_text.config(state=tk.DISABLED)  # Volver a deshabilitar la edición del segundo campo de texto

def compilar():
    global tokens
    global tabla
    cont=0
    val = False
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
    mensaje_text.delete("1.0", tk.END)  # Borrar el contenido anterior del mensaje
    escribir_tx2("Iniciando analisis...\n")
    tokens = analisis_lexico(texto)
    if tokens:
        for token in tokens:
            if val and token[0] == 'Id':
                valor2 = token[1]
                registro = {'dato1': valor1, 'dato2': valor2, 'dato3': 0}
                tabla.append(registro)
                val = False
            elif token[0] == 'TipodeDato':
                val = True
                valor1 = token[1]
            cont = cont+1
        analisis_sintactico(tokens)
        if not error_sintactico:
            escribir_tx2("Termino el analisis\n")
            correr_button.config(state=tk.NORMAL)
    print(tabla)

def cambio_texto(event):
    correr_button.config(state=tk.DISABLED)

def correr():
    if correr_button["state"] == tk.NORMAL:
        mensaje_text.config(state=tk.NORMAL)
        mensaje_text.insert(tk.END, "\nComienza a correr el programa:\n")
        mensaje_text.config(state=tk.DISABLED)

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
correr_button = tk.Button(marco_botones, text="Correr", font=("Arial Rounded MT Bold", 12), command=correr, relief=tk.RAISED, bd=2, state=tk.DISABLED)
correr_button.pack(side=tk.LEFT, padx=5)
correr_button.bind("<Button-1>", click)
correr_button.bind("<ButtonRelease-1>", liberar)
correr_button.bind("<Enter>", oscurecer)
correr_button.bind("<Leave>", restaurar)

ventana.bind("<Key>",cambio_texto)

# Ejecutar el bucle principal de la ventana
ventana.mainloop()