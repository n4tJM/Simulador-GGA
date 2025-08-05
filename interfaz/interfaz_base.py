import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from interfaz.panel_conceptos import PanelConceptos
from interfaz.panel_simulador import PanelSimulador
from interfaz.panel_visualizacion import PanelVisualizacion

class InterfazBase(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SIMULADOR GENÉTICO AVANZADO")
        self.geometry("1200x700")
        self.configure(bg='#f0f0f0')
        
        self.configurar_estilos()
        self.mostrar_interfaz_principal()
    
    def configurar_estilos(self):
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Nav.TButton', font=('Arial', 11), width=20, padding=10)
        self.style.configure('Nav.TFrame', background='#e0e0e0')
        self.style.configure('Content.TFrame', background='#ffffff')
        self.style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        self.style.configure('Desc.TLabel', font=('Arial', 10), wraplength=600)
    
    def mostrar_interfaz_principal(self):
        """Muestra la interfaz principal con panel de navegación y contenido"""
        # Limpiar widgets existentes
        for widget in self.winfo_children():
            widget.destroy()
        
        # Frame principal (contenedor horizontal)
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True)
        
        # Panel de navegación (izquierda)
        nav_frame = ttk.Frame(main_frame, style='Nav.TFrame', width=200)
        nav_frame.pack(side='left', fill='y', padx=5, pady=5)
        nav_frame.pack_propagate(False)
        
        # Panel de contenido (derecha)
        self.content_frame = ttk.Frame(main_frame, style='Content.TFrame')
        self.content_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        # Configurar encabezado del panel de navegación
        self.configurar_nav_header(nav_frame)
        
        # Botones de navegación
        ttk.Button(
            nav_frame, 
            text="Conceptos Básicos", 
            style='Nav.TButton',
            command=lambda: self.mostrar_contenido('conceptos')
        ).pack(pady=5, padx=10, fill='x')
        
        ttk.Button(
            nav_frame, 
            text="Simulador Genético", 
            style='Nav.TButton',
            command=lambda: self.mostrar_contenido('simulador')
        ).pack(pady=5, padx=10, fill='x')
        
        ttk.Button(
            nav_frame, 
            text="Visualización de Datos", 
            style='Nav.TButton',
            command=lambda: self.mostrar_contenido('visualizacion')
        ).pack(pady=5, padx=10, fill='x')
        
        # Mostrar contenido inicial
        self.mostrar_contenido('conceptos')
    
    def configurar_nav_header(self, parent):
        """Configura el encabezado del panel de navegación"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill='x', pady=10)
        
        try:
            logo_img = Image.open("img/logo.jpg")
            logo_img = logo_img.resize((80, 80), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            logo_label = ttk.Label(header_frame, image=self.logo)
            logo_label.pack(pady=5)
        except FileNotFoundError:
            logo_label = ttk.Label(header_frame, text="LOGO")
            logo_label.pack(pady=5)
        
        title_label = ttk.Label(
            header_frame, 
            text="MENÚ PRINCIPAL",
            style='Title.TLabel'
        )
        title_label.pack(pady=5)
    
    def mostrar_contenido(self, opcion):
        """Muestra el contenido correspondiente en el panel derecho"""
        # Limpiar contenido anterior
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Configurar el contenido según la opción seleccionada
        if opcion == 'conceptos':
            PanelConceptos(self.content_frame).pack(fill='both', expand=True, padx=20, pady=20)
        elif opcion == 'simulador':
            PanelSimulador(self.content_frame).pack(fill='both', expand=True, padx=20, pady=20)
        elif opcion == 'visualizacion':
            PanelVisualizacion(self.content_frame).pack(fill='both', expand=True, padx=20, pady=20)

if __name__ == "__main__":
    app = InterfazBase()
    app.mainloop()