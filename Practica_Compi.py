import tkinter as tk
import re
import math

current_token = 0
error_sintactico = False
error_semantico = False
tabla = []
lista_impresion = []

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
    ('Numero', r'\d+(\.\d+)?'),
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
    global current_token, error_sintactico
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
    parse_asigOimprimirOsqrt()
    match('}')

    # Verifica si se han procesado todos los tokens
    if current_token < len(tokens):
        escribir_tx2('Error de sintaxis. Token inesperado en la posición {}: {}\n'.format(
            current_token, tokens[current_token]))
        error_sintactico = True

def buscar_valor_id(id):
    for registro in tabla:
        if registro['dato2'] == id:
            return registro['dato3']
    return None

def actualizar_valor_id(id, valor):
    for registro in tabla:
        if registro['dato2'] == id:
            if registro['dato1'] == 'int':
                registro['dato3'] = int(valor)
            else:
                registro['dato3'] = valor
            break

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def procesar_asignacion(id, valor):
    global error_semantico
    valor_numerico = None
    if str(valor).isdigit():
        valor_numerico = int(valor)
    elif is_float(str(valor)):
        valor_numerico = float(valor)
    else:
        valor_id = buscar_valor_id(valor)
        if valor_id is not None:
            valor_numerico = valor_id

    if valor_numerico is not None:
        actualizar_valor_id(id, valor_numerico)
    else:
        escribir_tx2(f'Error semántico asignacion: El valor de la variable "{valor}" no está definido.')
        error_semantico = True

def procesar_sqrt(id):
    global error_semantico
    valor_id = buscar_valor_id(id)
    if valor_id is not None:
        raiz = math.sqrt(valor_id)
        actualizar_valor_id(id, raiz)
    else:
        escribir_tx2(f'Error semántico sqrt: El valor de la variable "{id}" no está definido.')
        error_semantico = True

def procesar_imprimir(texto):
    lista_impresion.append(texto)

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

# AsigOImprimirOSqrt -> Id Asignacion AsigOImprimir | Imprimir AsigOImprimir | Sqrt AsigOImprimir | ε
def parse_asigOimprimirOsqrt():
    if tokens[current_token][0] == 'Id':
        parse_asignacion()
        parse_asigOimprimirOsqrt()
    elif tokens[current_token][0] == 'imprimir':
        parse_imprimir()
        parse_asigOimprimirOsqrt()
    elif tokens[current_token][0] == 'sqrt':
        parse_sqrt()
        parse_asigOimprimirOsqrt()

# Sqrt -> sqrt(Id) ;
def parse_sqrt():
    if tokens[current_token][0] == 'sqrt':
        match('sqrt')
        match('(')
        id = tokens[current_token][1]
        match('Id')
        match(')')
        match(';')
        procesar_sqrt(id)

# Asignacion -> Id = Expresion ;
def parse_asignacion():
    if tokens[current_token][0] == 'Id':
        id = tokens[current_token][1]
        match('Id')
        match('=')
        expresion = parse_expresion()
        match(';')
        procesar_asignacion(id, expresion)

# Expresion -> Termino Expresion'
def parse_expresion():
    resultado = parse_termino()
    return parse_expresion_prime(resultado)

# Expresion' -> + Termino Expresion' | - Termino Expresion' | ε
def parse_expresion_prime(acumulador):
    if tokens[current_token][0] == '+':
        match('+')
        termino = parse_termino()
        return parse_expresion_prime(acumulador + termino)
    elif tokens[current_token][0] == '-':
        match('-')
        termino = parse_termino()
        return parse_expresion_prime(acumulador - termino)
    else:
        return acumulador

# Termino -> Factor Termino'
def parse_termino():
    resultado = parse_factor()
    return parse_termino_prime(resultado)

# Termino' -> * Factor Termino' | / Factor Termino' | ε
def parse_termino_prime(acumulador):
    if tokens[current_token][0] == '*':
        match('*')
        factor = parse_factor()
        return parse_termino_prime(acumulador * factor)
    elif tokens[current_token][0] == '/':
        match('/')
        factor = parse_factor()
        if factor != 0:
            return parse_termino_prime(acumulador / factor)
        else:
            escribir_tx2('Error semántico: División por cero.')
            return acumulador
    else:
        return acumulador

# Factor -> Numero | ( Expresion ) | Id
def parse_factor():
    global error_sintactico, error_semantico
    if tokens[current_token][0] == 'Numero':
        if tokens[current_token][1].isdigit():
            numero = int(tokens[current_token][1])
        elif is_float(tokens[current_token][1]):
            numero = float(tokens[current_token][1])
        match('Numero')
        return numero
    elif tokens[current_token][0] == '(':
        match('(')
        expresion = parse_expresion()
        match(')')
        return expresion
    elif tokens[current_token][0] == 'Id':
        id = tokens[current_token][1]
        match('Id')
        valor_id = buscar_valor_id(id)
        if valor_id is not None:
            return valor_id
        else:
            escribir_tx2(f'Error semántico parse_factor: El valor de la variable "{id}" no está definido.')
            error_semantico = True
            return 0
    else:
        escribir_tx2('Error de sintaxis. Token inesperado en la posición {}: {}\n'.format(
            current_token, tokens[current_token] if current_token < len(tokens) else 'EOF'))
        error_sintactico = True
        return 0

# Imprimir -> imprimir ( Texto Texto' ) ;
def parse_imprimir():
    match('imprimir')
    match('(')
    texto = parse_texto()
    texto = texto + str(parse_texto_prime())
    match(')')
    match(';')
    procesar_imprimir(texto)

# Texto -> Cadena | Id
def parse_texto():
    global error_sintactico, error_semantico
    if tokens[current_token][0] == 'Cadena':
        texto = tokens[current_token][1]
        texto = texto.replace('"', '')
        match('Cadena')
        return texto
    elif tokens[current_token][0] == 'Id':
        texto = tokens[current_token][1]
        match('Id')
        if buscar_valor_id(texto) is None:
            escribir_tx2(f'Error semántico parse_texto: El valor de la variable "{id}" no está definido.')
            error_semantico = True
        for registro in tabla:
            id = registro['dato2']
            valor = registro['dato3']
            texto = texto.replace(id, str(valor))
        return texto
    else:
        escribir_tx2('Error de sintaxis. Token inesperado en la posición {}: {}\n'.format(
            current_token, tokens[current_token] if current_token < len(tokens) else 'EOF'))
        error_sintactico = True
        return ''

# Texto' -> , Cadena Texto' | , Id Texto' | ε
def parse_texto_prime():
    global error_semantico
    if tokens[current_token][0] == ',':
        match(',')
        if tokens[current_token][0] == 'Cadena':
            texto = tokens[current_token][1]
            texto = texto.replace('"', '')
            match('Cadena')
            texto = texto + str(parse_texto_prime())
            return texto
        elif tokens[current_token][0] == 'Id':
            texto = tokens[current_token][1]
            match('Id')
            if buscar_valor_id(texto) is None:
                escribir_tx2(f'Error semántico parse_texto: El valor de la variable "{id}" no está definido.')
                error_semantico = True
            for registro in tabla:
                id = registro['dato2']
                valor = registro['dato3']
                texto = texto.replace(id, str(valor))
            texto = texto + str(parse_texto_prime())
            return texto
    return ''

def escribir_tx2(Text):
    mensaje_text.config(state=tk.NORMAL)  # Habilitar la edición del segundo campo de texto
    mensaje_text.insert(tk.END, Text)  # Agregar el nuevo mensaje
    mensaje_text.config(state=tk.DISABLED)  # Volver a deshabilitar la edición del segundo campo de texto

def compilar():
    global tokens, tabla, lista_impresion
    lista_impresion = []
    tabla = []
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
    mensaje_text.config(state=tk.NORMAL)  # Habilitar la edición del segundo campo de texto
    mensaje_text.delete("1.0", tk.END)# Borrar el contenido anterior del mensaje
    escribir_tx2("Iniciando analisis...\n")
    tokens = analisis_lexico(texto)
    if tokens:
        escribir_tx2("    Analisis lexico completado\n")
        for token in tokens:
            if val and token[0] == 'Id':
                valor2 = token[1]
                if valor1 == float:
                    registro = {'dato1': valor1, 'dato2': valor2, 'dato3': 0.0}
                else:
                    registro = {'dato1': valor1, 'dato2': valor2, 'dato3': 0}
                tabla.append(registro)
                val = False
            elif token[0] == 'TipodeDato':
                val = True
                valor1 = token[1]
        analisis_sintactico(tokens)
        if not error_sintactico and not error_semantico:
            escribir_tx2("    Analisis sintactico completado\n")
            escribir_tx2("    Analisis semantico completado\n")
            escribir_tx2("Termino el analisis\n")
            correr_button.config(state=tk.NORMAL)

def cambio_texto(event):
    correr_button.config(state=tk.DISABLED)

def correr():
    if correr_button["state"] == tk.NORMAL:
        escribir_tx2("\nComienza a correr el programa:\n")
        for impresion in lista_impresion:
            mensaje = impresion + "\n"
            escribir_tx2(mensaje)

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