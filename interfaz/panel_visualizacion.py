import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from interfaz.graficas_analisis import AnalizadorGraficas
import os
import pandas as pd

class PanelVisualizacion(ttk.Frame):
    def __init__(self, parent, csv_path="interfaz/Test.csv"):
        super().__init__(parent)
        self.available_datasets = {
            "Test": "interfaz/Test.csv",
            # Agregar más datasets aquí si es necesario
        }
        self.current_csv = csv_path
        self.analizador = AnalizadorGraficas(self.current_csv)
        self.configurar_interfaz()
    
    def configurar_interfaz(self):
        """Configura la interfaz del panel"""
        # Título
        ttk.Label(
            self, 
            text="VISUALIZACIÓN DE DATOS", 
            style='Title.TLabel'
        ).pack(anchor='w', pady=10)
        
        # Frame de control de datasets
        dataset_control_frame = ttk.Frame(self)
        dataset_control_frame.pack(fill='x', pady=5)
        
        # Selector de dataset
        ttk.Label(dataset_control_frame, text="Dataset:").pack(side='left', padx=5)
        
        self.dataset_var = tk.StringVar()
        self.dataset_combobox = ttk.Combobox(
            dataset_control_frame,
            textvariable=self.dataset_var,
            values=list(self.available_datasets.keys()),
            state="readonly",
            width=30
        )
        self.dataset_combobox.pack(side='left', padx=5)
        self.dataset_combobox.current(0)
        self.dataset_combobox.bind("<<ComboboxSelected>>", self.cambiar_dataset)
        
        # Botón para cargar nuevo dataset
        ttk.Button(
            dataset_control_frame,
            text="Cargar otro CSV",
            command=self.cargar_csv_externo
        ).pack(side='left', padx=5)
        
        # Información de la instancia
        self.info_frame = ttk.Frame(self)
        self.info_frame.pack(fill='x', pady=5)
        self.actualizar_info_instancia()
        
        # Selector de gráficos
        control_frame = ttk.Frame(self)
        control_frame.pack(fill='x', pady=10)
        
        ttk.Label(control_frame, text="Tipo de gráfico:").pack(side='left', padx=5)
        self.graph_combobox = ttk.Combobox(control_frame, values=[
            "Matriz de correlación",
            "Gráfico de cajas (Random min vs jobs)",
            "Gráfico de cajas (Random best vs jobs)",
            "Gráfico de cajas (DFB vs jobs)",
            "Gráfico de cajas (DFM vs jobs)",
            "Gráfico de dispersión (CV vs Random min)",
            "Gráfico de dispersión (CV vs Random best)",
            "Gráfico de dispersión (CV vs DFB)",
            "Gráfico de dispersión (CV vs DFM)",
            "Gráfico de violín (Random min)",
            "Gráfico de violín (Random best)",
            "Gráfico de violín (DFB)",
            "Gráfico de violín (DFM)",
            "Análisis PCA (2 componentes)",
            "Gráfico de líneas (Evolución)"
        ], state="readonly", width=30)
        self.graph_combobox.pack(side='left', padx=5)
        
        ttk.Button(
            control_frame, 
            text="Generar Gráfico", 
            command=self.mostrar_grafico,
            style='Accent.TButton'
        ).pack(side='left', padx=10)
        
        # Frame para el gráfico
        self.graph_frame = ttk.Frame(self)
        self.graph_frame.pack(fill='both', expand=True, pady=10)
        
        # Mensaje inicial
        ttk.Label(
            self.graph_frame, 
            text="Seleccione el tipo de gráfico a visualizar",
            font=('Arial', 10, 'italic')
        ).pack(expand=True)
    
    def actualizar_info_instancia(self):
        """Actualiza la información mostrada sobre la instancia cargada"""
        for widget in self.info_frame.winfo_children():
            widget.destroy()
        
        ttk.Label(
            self.info_frame, 
            text=f"Instancia cargada: {os.path.basename(self.current_csv)}",
            font=('Arial', 9)
        ).pack(side='left')
    
    def cambiar_dataset(self, event=None):
        """Cambia el dataset actual según la selección del combobox"""
        selected_name = self.dataset_var.get()
        if selected_name in self.available_datasets:
            self.current_csv = self.available_datasets[selected_name]
            self.analizador = AnalizadorGraficas(self.current_csv)
            self.actualizar_info_instancia()
            messagebox.showinfo("Info", f"Dataset cambiado a: {selected_name}")
    
    def cargar_csv_externo(self):
        """Permite al usuario cargar un archivo CSV externo"""
        filepath = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filepath:
            try:
                # Verificar si es un archivo CSV válido
                pd.read_csv(filepath)
                
                # Agregar a los datasets disponibles
                filename = os.path.basename(filepath)
                self.available_datasets[filename] = filepath
                
                # Actualizar el combobox
                self.dataset_combobox['values'] = list(self.available_datasets.keys())
                self.dataset_combobox.set(filename)
                
                # Cambiar al nuevo dataset
                self.current_csv = filepath
                self.analizador = AnalizadorGraficas(self.current_csv)
                self.actualizar_info_instancia()
                
                messagebox.showinfo("Éxito", f"Archivo {filename} cargado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
    
    def mostrar_grafico(self):
        """Muestra el gráfico seleccionado"""
        if not self.graph_combobox.get():
            messagebox.showwarning("Advertencia", "Seleccione un tipo de gráfico")
            return
        
        # Limpiar frame del gráfico
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        try:
            tipo_grafico = self.graph_combobox.get()
            
            if tipo_grafico == "Matriz de correlación":
                fig = self.analizador.matriz_correlacion()
            elif tipo_grafico == "Gráfico de cajas (Random min vs jobs)":
                fig = self.analizador.boxplot_tiempos(algoritmo='Random min')
            elif tipo_grafico == "Gráfico de cajas (Random best vs jobs)":
                fig = self.analizador.boxplot_tiempos(algoritmo='Random best')
            elif tipo_grafico == "Gráfico de cajas (DFB vs jobs)":
                fig = self.analizador.boxplot_tiempos(algoritmo='Diff_fastest best-t-min')
            elif tipo_grafico == "Gráfico de cajas (DFM vs jobs)":
                fig = self.analizador.boxplot_tiempos(algoritmo='Diff_fastest min')
            elif tipo_grafico == "Gráfico de dispersión (CV vs Random min)":
                fig = self.analizador.dispersion_cv_tiempo(algoritmo='Random min')
            elif tipo_grafico == "Gráfico de dispersión (CV vs Random best)":
                fig = self.analizador.dispersion_cv_tiempo(algoritmo='Random best')
            elif tipo_grafico == "Gráfico de dispersión (CV vs DFB)":
                fig = self.analizador.dispersion_cv_tiempo(algoritmo='Diff_fastest best-t-min')
            elif tipo_grafico == "Gráfico de dispersión (CV vs DFM)":
                fig = self.analizador.dispersion_cv_tiempo(algoritmo='Diff_fastest min')
            elif tipo_grafico == "Gráfico de violín (Random min)":
                fig = self.analizador.grafico_violin(algoritmo='Random min')
            elif tipo_grafico == "Gráfico de violín (Random best)":
                fig = self.analizador.grafico_violin(algoritmo='Random best')
            elif tipo_grafico == "Gráfico de violín (DFB)":
                fig = self.analizador.grafico_violin(algoritmo='Diff_fastest best-t-min')
            elif tipo_grafico == "Gráfico de violín (DFM)":
                fig = self.analizador.grafico_violin(algoritmo='Diff_fastest min')
            elif tipo_grafico == "Análisis PCA (2 componentes)":
                fig = self.analizador.analisis_pca()
            elif tipo_grafico == "Gráfico de líneas (Evolución)":
                fig = self.analizador.grafico_lineas()
            
            # Mostrar gráfico
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el gráfico:\n{str(e)}")
            ttk.Label(
                self.graph_frame, 
                text="Error al generar el gráfico. Verifique los datos.",
                font=('Arial', 10, 'italic')
            ).pack(expand=True)