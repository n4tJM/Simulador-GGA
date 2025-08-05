import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from interfaz.simulador_genetico import SimuladorGenetico

class PanelSimulador(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configurar_interfaz()
    
    def configurar_interfaz(self):
        # Título
        ttk.Label(
            self, 
            text="SIMULADOR GENÉTICO", 
            style='Title.TLabel'
        ).pack(anchor='w', pady=10)
        
        # Descripción
        desc_text = """
        Esta herramienta permite ejecutar algoritmos genéticos. 
        Podrá configurar todos los parámetros del algoritmo, cargar 
        instancias de problemas y visualizar los resultados de la ejecución.
        
        El simulador incluye diferentes operadores de cruza, mutación.
        """
        
        ttk.Label(
            self, 
            text=desc_text,
            style='Desc.TLabel',
            justify='left'
        ).pack(anchor='w', fill='x', pady=10)
        
        # Botón para ir al simulador
        ttk.Button(
            self, 
            text="Iniciar Simulador", 
            command=self.iniciar_simulador,
            style='Accent.TButton'
        ).pack(pady=20)
    
    def iniciar_simulador(self):
        # Limpiar el frame actual
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Mostrar el simulador en el mismo espacio
        SimuladorGenetico(self.parent).pack(fill='both', expand=True)