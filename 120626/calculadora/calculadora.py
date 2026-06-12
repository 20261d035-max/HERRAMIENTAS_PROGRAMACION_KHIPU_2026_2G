import tkinter as tk
from tkinter import messagebox

class CalculadoraPink:
    def __init__(self, root):
        self.root = root
        self.root.title("Pink Calc ✨")
        self.root.geometry("360x520")
        self.root.configure(bg="#FFE4E1")  # Fondo principal: Misty Rose (Rosado pastel suave)
        self.root.resizable(False, False)   # Ventana de tamaño fijo para mantener el diseño limpio

        # Variables de control
        self.expresion = ""
        self.pantalla_var = tk.StringVar()

        # Paleta de colores (Tema Rosado)
        self.COLOR_FONDO = "#FFE4E1"       # Rosado pastel fondo
        self.COLOR_PANTALLA = "#FFF0F5"    # Lavanda/Rosado ultra claro para la pantalla
        self.COLOR_NUMEROS = "#FFFFFF"     # Botones numéricos blancos
        self.COLOR_TEXTO_NUM = "#D87093"   # Texto de números: Pale Violet Red
        self.COLOR_OPERADORES = "#FF69B4"  # Botones de operación: Hot Pink
        self.COLOR_IGUAL = "#FF1493"       # Botón de igual: Deep Pink
        self.COLOR_BORRAR = "#FFB6C1"      # Botón de borrar: Light Pink
        self.COLOR_TEXTO_LIGHT = "#FFFFFF" # Texto blanco para botones vibrantes
        
        # Inicializar los componentes de la interfaz
        self.crear_pantalla()
        self.crear_botones()

    def crear_pantalla(self):
        """Crea la zona donde se muestran los números y resultados."""
        # Contenedor para darle un margen estético a la pantalla
        frame_pantalla = tk.Frame(self.root, bg=self.COLOR_FONDO, pady=15)
        frame_pantalla.pack(expand=True, fill="both")

        pantalla = tk.Entry(
            frame_pantalla, 
            textvariable=self.pantalla_var, 
            font=("Segoe UI", 26, "bold"), 
            bg=self.COLOR_PANTALLA, 
            fg="#4A4A4A", 
            bd=0, 
            justify="right",
            insertbackground="#D87093" # Color del cursor
        )
        # Añadimos un pequeño padding interno simulado con ipady
        pantalla.pack(padx=20, fill="both", ipady=15)

    def crear_botones(self):
        """Crea la cuadrícula de botones con el diseño solicitado."""
        # Contenedor para la cuadrícula de botones
        frame_botones = tk.Frame(self.root, bg=self.COLOR_FONDO)
        frame_botones.pack(expand=True, fill="both", padx=15, pady=(0, 15))

        # Configuración de pesos de filas y columnas para que sean proporcionales
        for i in range(5):
            frame_botones.rowconfigure(i, weight=1)
        for j in range(4):
            frame_botones.columnconfigure(j, weight=1)

        # Definición de los botones: (Texto, Fila, Columna, Color Fondo, Color Texto)
        botones = [
            ('C', 0, 0, self.COLOR_BORRAR, self.COLOR_TEXTO_LIGHT),
            ('/', 0, 3, self.COLOR_OPERADORES, self.COLOR_TEXTO_LIGHT),
            ('*', 1, 3, self.COLOR_OPERADORES, self.COLOR_TEXTO_LIGHT),
            ('-', 2, 3, self.COLOR_OPERADORES, self.COLOR_TEXTO_LIGHT),
            ('+', 3, 3, self.COLOR_OPERADORES, self.COLOR_TEXTO_LIGHT),
            ('=', 4, 3, self.COLOR_IGUAL, self.COLOR_TEXTO_LIGHT),
            ('7', 1, 0, self.COLOR_NUMEROS, self.COLOR_TEXTO_NUM),
            ('8', 1, 1, self.COLOR_NUMEROS, self.COLOR_TEXTO_NUM),
            ('9', 1, 2, self.COLOR_NUMEROS, self.COLOR_TEXTO_NUM),
            ('4', 2, 0, self.COLOR_NUMEROS, self.COLOR_TEXTO_NUM),
            ('5', 2, 1, self.COLOR_NUMEROS, self.COLOR_TEXTO_NUM),
            ('6', 2, 2, self.COLOR_NUMEROS, self.COLOR_TEXTO_NUM),
            ('1', 3, 0, self.COLOR_NUMEROS, self.COLOR_TEXTO_NUM),
            ('2', 3, 1, self.COLOR_NUMEROS, self.COLOR_TEXTO_NUM),
            ('3', 3, 2, self.COLOR_NUMEROS, self.COLOR_TEXTO_NUM),
            ('0', 4, 0, self.COLOR_NUMEROS, self.COLOR_TEXTO_NUM),
            ('.', 4, 1, self.COLOR_NUMEROS, self.COLOR_TEXTO_NUM),
        ]

        # Renderizar los botones en la interfaz
        for texto, fila, col, bg_color, fg_color in botones:
            # Caso especial: El botón '0' o el botón 'C' pueden expandirse si lo deseas, 
            # aquí el botón '0' ocupa una celda normal, pero hacemos que el '.' y '0' se alineen.
            # Para el botón '=', si quisieras expandirlo, puedes usar columnspan.
            
            # Ajuste dinámico para botones especiales (Ej: 'C' ocupa 3 columnas para un look más limpio)
            colspan = 3 if texto == 'C' else 1
            
            btn = tk.Button(
                frame_botones,
                text=texto,
                font=("Segoe UI", 16, "bold"),
                bg=bg_color,
                fg=fg_color,
                bd=0,
                activebackground=self.COLOR_FONDO, # Evita el flash gris horrible de Windows al hacer clic
                activeforeground=fg_color,
                cursor="hand2",
                command=lambda t=texto: self.al_hacer_clic(t)
            )
            btn.grid(row=fila, column=col, columnspan=colspan, sticky="nsew", padx=4, pady=4)
            
            # Efecto Hover (Cambio sutil de color al pasar el ratón)
            self.añadir_efecto_hover(btn, bg_color)

    def añadir_efecto_hover(self, boton, color_original):
        """Genera un efecto visual aclarando u oscureciendo el botón al pasar el mouse."""
        # Si el color es blanco, el hover será un rosa muy tierno, si no, se oscurece un poco
        color_hover = "#FFF0F5" if color_original == "#FFFFFF" else "#E066A9"
        if color_original == "#FF1493": color_hover = "#C71585" # Hover del botón igual
        if color_original == "#FFB6C1": color_hover = "#FFA07A" # Hover de borrar

        boton.bind("<Enter>", lambda e: boton.config(bg=color_hover))
        boton.bind("<Leave>", lambda e: boton.config(bg=color_original))

    def al_hacer_clic(self, boton_presionado):
        """Manejador de eventos para los clics de los botones."""
        if boton_presionado == 'C':
            self.expresion = ""
            self.pantalla_var.set("")
            
        elif boton_presionado == '=':
            try:
                # El manejo de errores evita que el programa colapse
                # eval() evalúa la cadena matemática directamente
                if self.expresion:
                    resultado = str(eval(self.expresion))
                    
                    # Formatear si el resultado es un entero flotante (ej: 5.0 -> 5)
                    if resultado.endswith('.0'):
                        resultado = resultado[:-2]
                        
                    self.pantalla_var.set(resultado)
                    self.expresion = resultado # Permitir seguir operando con el resultado
            except ZeroDivisionError:
                messagebox.showerror("Error", "¡No se puede dividir entre cero! 💕")
                self.limpiar_pantalla_error()
            except Exception:
                messagebox.showerror("Error", "Operación inválida")
                self.limpiar_pantalla_error()
                
        else:
            # Añadir el número o el operador a la expresión actual
            self.expresion += str(boton_presionado)
            self.pantalla_var.set(self.expresion)

    def limpiar_pantalla_error(self):
        """Limpia las variables en caso de un error matemático."""
        self.expresion = ""
        self.pantalla_var.set("")


# Bloque de ejecución principal para Visual Studio Code
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraPink(root)
    root.mainloop()