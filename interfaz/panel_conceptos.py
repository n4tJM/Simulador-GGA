import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class PanelConceptos(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.topics = {
            "Población inicial": {
                "desc": "Conjunto inicial de soluciones candidatas para el problema.",
                "has_operators": False
            },
            "Clonación": {
                "desc": "Proceso de copiar individuos sin modificación para la siguiente generación.",
                "has_operators": False
            },
            "Selección": {
                "desc": "Mecanismo para elegir qué individuos participarán en la reproducción.",
                "has_operators": False
            },
            "Mutación": {
                "desc": "Operador que introduce cambios aleatorios para mantener diversidad genética.",
                "has_operators": True,
                "operators": {
                    "Swap": "img/muta/muta_swap.jpg",
                    "Insercion": "img/muta/muta_insertion.jpg",
                    "Item Elimantion": "img/muta/muta_item_elimination.jpg",
                    "Eliminacion": "img/muta/muta_elimination.jpg",
                    "Fusion y division": "img/muta/muta_merge_split.jpg",
                }
            },
            "Cruza": {
                "desc": "Combinación de características de dos individuos para crear descendencia.",
                "has_operators": True,
                "operators": {
                    "Un punto": "img/cruza/cruza_1px.jpg",
                    "Dos puntos": "img/cruza/cruza_2px.jpg",
                    "Tres puntos": "img/cruza/cruza_3px.jpg",
                    "Cuatro puntos": "img/cruza/cruza_4px.jpg",
                    "Multi-puntos": "img/cruza/cruza_multipx.jpg",
                    "Uniforme": "img/cruza/cruza_ux.jpg",
                    "Reorganizacion de exones": "img/cruza/cruza_esx.JPG",
                    "Gene-level": "img/cruza/cruza_glx.jpg",
                    "Greddy partition": "img/cruza/cruza_gpx.jpg"
                }
            },
            "Condición de paro": {
                "desc": "Criterios para determinar cuándo finalizar el algoritmo genético.",
                "has_operators": False
            },
            "Remplazo": {
                "desc": "Estrategia para actualizar la población entre generaciones.",
                "has_operators": False
            }
        }
        self.selected_topic = tk.StringVar()
        self.current_image = None
        self.original_image = None
        self.scaled_image = None
        self.zoom_level = 1.0
        self.min_zoom = 0.5
        self.max_zoom = 3.0
        self.zoom_factor = 1.2
        self.config_interfaz()

    def config_interfaz(self):
        # Frame principal con dos columnas
        content_frame = ttk.Frame(self)
        content_frame.pack(fill='both', expand=True)
        
        # Columna izquierda - Selector de temas
        topics_frame = ttk.LabelFrame(content_frame, text="Conceptos Básicos", width=250, padding="15")
        topics_frame.pack(side='left', fill='y', padx=5, pady=5)
        
        for topic in self.topics:
            rb = ttk.Radiobutton(
                topics_frame, 
                text=topic, 
                variable=self.selected_topic, 
                value=topic, 
                command=self._update_topic_display
            )
            rb.pack(anchor='w', padx=5, pady=2)
        
        # Frame para contenido derecho
        self.right_frame = ttk.Frame(content_frame)
        self.right_frame.pack(side='right', fill='both', expand=True)
        
        # Descripción (siempre visible)
        self.desc_frame = ttk.LabelFrame(self.right_frame, text="Descripción", padding="10")
        self.desc_frame.pack(fill='x', pady=5)
        
        self.desc_text = tk.Text(self.desc_frame, wrap='word', height=4, font=('Arial', 10))
        self.desc_text.pack(fill='x')
        self.desc_text.config(state='disabled')
        
        # Selector de operadores (inicialmente oculto)
        self.operator_frame = ttk.LabelFrame(self.right_frame, text="Seleccione Operador", padding="10")
        
        self.operator_combobox = ttk.Combobox(self.operator_frame, state='readonly')
        self.operator_combobox.pack(fill='x')
        self.operator_combobox.bind('<<ComboboxSelected>>', self._update_example_display)
        
        # Área de ejemplo con scroll y zoom
        self.example_frame = ttk.LabelFrame(self.right_frame, text="Ejemplo", padding="10")
        
        # Frame contenedor para canvas y scrollbars
        self.example_container = ttk.Frame(self.example_frame)
        self.example_container.pack(fill='both', expand=True)
        
        # Scrollbars vertical y horizontal
        self.v_scroll = ttk.Scrollbar(self.example_container, orient='vertical')
        self.h_scroll = ttk.Scrollbar(self.example_container, orient='horizontal')
        
        # Canvas para la imagen con scrollbars
        self.example_canvas = tk.Canvas(
            self.example_container,
            yscrollcommand=self.v_scroll.set,
            xscrollcommand=self.h_scroll.set,
            bg='white'
        )
        
        # Configurar scrollbars
        self.v_scroll.config(command=self.example_canvas.yview)
        self.h_scroll.config(command=self.example_canvas.xview)
        
        # Grid layout para los elementos
        self.example_canvas.grid(row=0, column=0, sticky='nsew')
        self.v_scroll.grid(row=0, column=1, sticky='ns')
        self.h_scroll.grid(row=1, column=0, sticky='ew')
        
        # Configurar expansión del grid
        self.example_container.columnconfigure(0, weight=1)
        self.example_container.rowconfigure(0, weight=1)
        
        # Frame interno para la imagen (se agregará al canvas)
        self.image_frame = ttk.Frame(self.example_canvas)
        self.image_id = self.example_canvas.create_window((0, 0), window=self.image_frame, anchor='nw')
        
        # Label para mostrar la imagen
        self.example_label = ttk.Label(self.image_frame)
        self.example_label.pack()
        
        # Configurar eventos para el zoom
        self.example_canvas.bind('<MouseWheel>', self._on_mousewheel)  # Windows/Linux
        self.example_canvas.bind('<Button-4>', self._on_mousewheel)    # Linux (up)
        self.example_canvas.bind('<Button-5>', self._on_mousewheel)    # Linux (down)
        
        # Configuración inicial
        self.selected_topic.set(next(iter(self.topics)))
        self._update_topic_display()
    
    def _on_mousewheel(self, event):
        """Manejador para el zoom con rueda del mouse"""
        if event.delta > 0 or event.num == 4:  # Zoom in
            self._zoom_image(self.zoom_factor)
        elif event.delta < 0 or event.num == 5:  # Zoom out
            self._zoom_image(1/self.zoom_factor)
    
    def _zoom_image(self, factor):
        """Aplica zoom a la imagen"""
        if not hasattr(self, 'original_image'):
            return
            
        new_zoom = self.zoom_level * factor
        
        # Limitar el rango de zoom
        if new_zoom < self.min_zoom or new_zoom > self.max_zoom:
            return
        
        self.zoom_level = new_zoom
        
        # Escalar la imagen
        width = int(self.original_image.width * self.zoom_level)
        height = int(self.original_image.height * self.zoom_level)
        resized_img = self.original_image.resize((width, height), Image.LANCZOS)
        self.scaled_image = ImageTk.PhotoImage(resized_img)
        
        # Actualizar la imagen en el label
        self.example_label.config(image=self.scaled_image)
        self.example_label.image = self.scaled_image
        
        # Actualizar el tamaño del frame interno
        self.image_frame.config(width=width, height=height)
        self.example_canvas.itemconfig(self.image_id, width=width, height=height)
        
        # Actualizar el área de scroll
        self.example_canvas.configure(scrollregion=self.example_canvas.bbox('all'))
    
    def _update_topic_display(self):
        topic = self.selected_topic.get()
        topic_data = self.topics[topic]
        
        # Actualizar descripción
        self.desc_text.config(state='normal')
        self.desc_text.delete(1.0, 'end')
        self.desc_text.insert('end', topic_data["desc"])
        self.desc_text.config(state='disabled')
        
        # Mostrar u ocultar elementos según el tema
        if topic_data["has_operators"]:
            if not self.operator_frame.winfo_ismapped():
                self.operator_frame.pack(fill='x', pady=5)
                self.example_frame.pack(fill='both', expand=True, pady=5)
            
            self.operator_combobox['values'] = list(topic_data["operators"].keys())
            self.operator_combobox.set(next(iter(topic_data["operators"].keys())))
            self._update_example_display()
        else:
            if self.operator_frame.winfo_ismapped():
                self.operator_frame.pack_forget()
                self.example_frame.pack_forget()
    
    def _update_example_display(self, event=None):
        topic = self.selected_topic.get()
        if not self.topics[topic]["has_operators"]:
            return
        
        selected_operator = self.operator_combobox.get()
        image_path = self.topics[topic]["operators"][selected_operator]
        
        try:
            # Resetear zoom
            self.zoom_level = 1.0
            
            # Cargar imagen original
            self.original_image = Image.open(image_path)
            
            # Mostrar imagen inicial (sin zoom)
            resized_img = self.original_image.copy()
            resized_img.thumbnail((1200, 600), Image.LANCZOS)
            self.scaled_image = ImageTk.PhotoImage(resized_img)
            
            self.example_label.config(image=self.scaled_image)
            self.example_label.image = self.scaled_image
            
            # Configurar tamaño del frame interno
            self.image_frame.config(width=resized_img.width, height=resized_img.height)
            self.example_canvas.itemconfig(
                self.image_id, 
                width=resized_img.width, 
                height=resized_img.height
            )
            
            # Actualizar área de scroll
            self.example_canvas.configure(scrollregion=self.example_canvas.bbox('all'))
            
        except Exception as e:
            self.example_label.config(
                text=f"Error cargando imagen: {str(e)}",
                foreground='red'
            )