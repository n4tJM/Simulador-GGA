import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from simulador.genetic_algorithm import GeneticAlgorithm
from simulador.solution import Solution
from interfaz.data import GetData
from interfaz.features import extract_features
 

class SimuladorGenetico(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.ga = None
        self.datos_csv = None
        self.ejecutando = False
        self.historial_fitness = []
        self.configurar_interfaz()
    
    def configurar_interfaz(self):
        self.configure(style='TFrame')
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Frame superior para parámetros
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill='x', pady=(0, 20))
        
        # Frame izquierdo (configuración)
        config_frame = ttk.LabelFrame(top_frame, text="Configuración", padding=15)
        config_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        # Frame derecho (vista previa)
        preview_frame = ttk.LabelFrame(top_frame, text="Vista Previa", padding=15)
        preview_frame.pack(side='right', fill='both', expand=True, padx=5)
        
        # Configuración de parámetros
        self.configurar_parametros(config_frame)
        
        # Configuración de vista previa
        self.configurar_vista_previa(preview_frame)
        
        # Frame inferior para botones y progreso
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill='x', pady=(10, 0))
        
        # Botones
        self.configurar_botones(bottom_frame)
        
        # Barra de estado
        self.status_var = tk.StringVar(value="Listo")
        status_bar = ttk.Label(bottom_frame, textvariable=self.status_var, relief='sunken')
        status_bar.pack(fill='x', pady=(10, 0))
    
    def configurar_parametros(self, parent):
        # Tamaño población
        ttk.Label(parent, text="Tamaño población:").grid(row=0, column=0, sticky='e', padx=5, pady=2)
        self.poblacion_var = tk.StringVar(value="100")
        ttk.Entry(parent, textvariable=self.poblacion_var, width=10).grid(row=0, column=1, sticky='w', pady=2)
        
        # Generaciones
        ttk.Label(parent, text="N° Generaciones:").grid(row=1, column=0, sticky='e', padx=5, pady=2)
        self.generaciones_var = tk.StringVar(value="100")
        ttk.Entry(parent, textvariable=self.generaciones_var, width=10).grid(row=1, column=1, sticky='w', pady=2)
        
        # Tasa cruza
        ttk.Label(parent, text="Tasa cruza:").grid(row=2, column=0, sticky='e', padx=5, pady=2)
        self.cruza_var = tk.StringVar(value="0.8")
        ttk.Entry(parent, textvariable=self.cruza_var, width=10).grid(row=2, column=1, sticky='w', pady=2)
        
        # Tasa mutación
        ttk.Label(parent, text="Tasa mutación:").grid(row=3, column=0, sticky='e', padx=5, pady=2)
        self.mutacion_var = tk.StringVar(value="0.2")
        ttk.Entry(parent, textvariable=self.mutacion_var, width=10).grid(row=3, column=1, sticky='w', pady=2)
        
        # Operadores
        ttk.Label(parent, text="Operador cruza:").grid(row=4, column=0, sticky='e', padx=5, pady=2)
        self.operador_cruza = ttk.Combobox(parent, values=["UniformCrossover", "OnePointCrossover", "TwoPointCrossover",
        "ThreePointCrossover", "FourPointCrossover", "MultiPointCrossover", "ReplacementWorst"], state="readonly")
        self.operador_cruza.set("UniformCrossover")
        self.operador_cruza.grid(row=4, column=1, sticky='w', pady=2)
        
        ttk.Label(parent, text="Operador mutación:").grid(row=5, column=0, sticky='e', padx=5, pady=2)
        self.operador_mutacion = ttk.Combobox(parent, values=["SwapMutation", "InsertionMutation", "ItemEliminationMutation",
                                                              "EliminationMutation", "MergeAndSplitMutation", "ESXMutation"], state="readonly")
        self.operador_mutacion.set("SwapMutation")
        self.operador_mutacion.grid(row=5, column=1, sticky='w', pady=2)
        
        # Selección de archivo
        ttk.Label(parent, text="Archivo CSV:").grid(row=6, column=0, sticky='e', padx=5, pady=2)
        self.file_path = ttk.Label(parent, text="Ningún archivo seleccionado", width=20)
        self.file_path.grid(row=6, column=1, sticky='w', pady=2)
        ttk.Button(parent, text="Examinar", command=self.seleccionar_csv, width=10).grid(row=6, column=2, padx=5)
    
    def configurar_vista_previa(self, parent):
        self.tree = ttk.Treeview(parent, height=8)
        self.tree.pack(fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Configurar columnas iniciales
        self.tree["columns"] = ("info",)
        self.tree.heading("#0", text="Ítem")
        self.tree.heading("info", text="Seleccione un archivo CSV")
        self.tree.column("#0", width=50)
        self.tree.column("info", width=200)
    
    def configurar_botones(self, parent):
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill='x', pady=10)
        
        # Botón Volver
        ttk.Button(
            btn_frame, 
            text="Volver", 
            command=self.volver_a_principal,
            style='TButton',
            width=15
        ).pack(side='left', padx=10)
        
        # Espacio intermedio
        ttk.Frame(btn_frame).pack(side='left', expand=True)
        
        # Botón Ejecutar
        ttk.Button(
            btn_frame, 
            text="Ejecutar Algoritmo", 
            command=self.ejecutar_algoritmo,
            style='Accent.TButton',
            width=15
        ).pack(side='right', padx=10)
    
    def seleccionar_csv(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filepath:
            self.file_path.config(text=filepath.split('/')[-1])
            self.cargar_csv(filepath)
    
    def cargar_csv(self, filepath):
        try:
            self.datos_csv, self.n_jobs, self.n_machines = GetData(filepath)
            instance_name = filepath.split('/')[-1]

            self.features = extract_features(
                data=self.datos_csv,
                n=self.n_jobs,
                m=self.n_machines,
                instance_name=instance_name
            )

            features_str = f"Jobs: {self.n_jobs}, Máquinas: {self.n_machines} | q: {self.features['q']:.2f} | CV: {self.features['cv_pij']:.2f}%"
            self.status_var.set(f"Archivo cargado: {features_str}")

            # Mostrar vista previa
            for item in self.tree.get_children():
                self.tree.delete(item)

            columnas = [f"Máquina {i+1}" for i in range(self.n_machines)]
            self.tree["columns"] = columnas
            self.tree["show"] = "headings"

            for col in columnas:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=80, anchor='center')

            for i in range(min(10, len(self.datos_csv))):
                self.tree.insert("", "end", values=self.datos_csv[i])

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
            self.datos_csv = None
            self.status_var.set("Error al cargar archivo")
    
    def volver_a_principal(self):
        if self.ejecutando:
            if not messagebox.askyesno("Confirmar", "El algoritmo está en ejecución. ¿Desea detenerlo y volver?"):
                return
            self.ejecutando = False
        
        self.pack_forget()
        self.parent.mostrar_interfaz_principal()
    
    def ejecutar_algoritmo(self):
        if self.datos_csv is None:
            messagebox.showwarning("Advertencia", "Debe seleccionar un archivo CSV primero")
            return
        
        try:
            n_jobs = len(self.datos_csv)
            n_machines = len(self.datos_csv[0]) if n_jobs > 0 else 0
            

            # Configurar algoritmo genético
            self.ga = GeneticAlgorithm(
                instance=self.datos_csv,
                n_jobs=self.n_jobs,
                n_machines=self.n_machines,
                p_size=int(self.poblacion_var.get()),
                p_gen=int(self.generaciones_var.get()),
                c_rate=float(self.cruza_var.get()),
                m_rate=float(self.mutacion_var.get())
            )

            # Inicializar población
            self.ga.run()
            self.historial_fitness = [self.ga.best_solution.fitness]

            self.status_var.set("Configurando algoritmo genético...")  
            
            # Mostrar ventana de progreso
            self.mostrar_progreso()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al configurar el algoritmo:\n{str(e)}")
            self.status_var.set("Error en configuración")
    
    def mostrar_progreso(self):
        self.progress_window = tk.Toplevel(self)
        self.progress_window.title("Ejecutando del Algoritmo Genético")
        self.progress_window.geometry("400x100")
        
        # Botones
        btn_frame = ttk.Frame(self.progress_window)
        btn_frame.pack(fill='x', pady=10)
        
        ttk.Button(
            btn_frame, 
            text="Detener", 
            command=self.detener_algoritmo,
            style='TButton'
        ).pack(side='left', padx=20)
        
        ttk.Button(
            btn_frame, 
            text="Ver Resultados", 
            command=self.mostrar_resultados,
            style='Accent.TButton',
            state='disabled'
        ).pack(side='right', padx=20)
        
        self.result_btn = btn_frame.winfo_children()[1]
        
        # Iniciar ejecución
        self.ejecutando = True
        self.ejecutar_generaciones()
    
    def ejecutar_generaciones(self):
        if not self.ejecutando or self.ga.generation >= self.ga.max_generations:
            self.finalizar_ejecucion()
            return
        
        # Ejecutar una generación
        self.ga.run_generation()
        self.historial_fitness.append(self.ga.best_solution.fitness)
        
        # Actualizar interfaz
        self.gen_label.config(text=str(self.ga.generation))
        self.fitness_label.config(text=f"{self.ga.best_solution.fitness:.2f}")
        
        # Actualizar gráfico
        self.line.set_data(range(len(self.historial_fitness)), self.historial_fitness)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()
        
        # Programar próxima generación
        self.progress_window.after(100, self.ejecutar_generaciones)
    
    def detener_algoritmo(self):
        self.ejecutando = False
        self.finalizar_ejecucion()
    
    def finalizar_ejecucion(self):
        self.result_btn.config(state='normal')
        self.status_var.set(f"Ejecución completada - Mejor fitness: {self.ga.best_solution.fitness:.2f}")
    
    def mostrar_resultados(self):
        if not hasattr(self, 'ga') or not self.ga.best_solution:
            return
        
        result_window = tk.Toplevel(self)
        result_window.title("Resultados del Algoritmo Genético")
        result_window.geometry("600x300")
        
        # Frame principal
        main_frame = ttk.Frame(result_window)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Notebook para pestañas
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)
        
        # Pestaña 1: Resultados del algoritmo
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Resultados")
        
        # Pestaña 2: Características de la instancia
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Características")
        
        # Contenido pestaña 1 (resultados)
        self._crear_pestana_resultados(tab1)
        
        # Contenido pestaña 2 (características)
        self._crear_pestana_caracteristicas(tab2)
        
        # Frame para botones adicionales
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=10)
        
        # Botón para exportar datos
        ttk.Button(
            btn_frame, 
            text="Exportar Datos a CSV", 
            command=self.exportar_datos,
            style='Accent.TButton'
        ).pack(side='left', padx=10)
        
        # Botón cerrar
        ttk.Button(
            btn_frame, 
            text="Cerrar", 
            command=result_window.destroy,
            style='TButton'
        ).pack(side='right', padx=10)

    def _crear_pestana_resultados(self, parent):
        """Crea el contenido de la pestaña de resultados"""
        # Frame para información general
        info_frame = ttk.LabelFrame(parent, text="Resumen de Ejecución", padding=10)
        info_frame.pack(fill='x', pady=(0, 10), padx=5)
        
        # Información básica
        ttk.Label(info_frame, text=f"Mejor Fitness: {self.ga.best_solution.fitness:.2f}").pack(anchor='w')
        ttk.Label(info_frame, text=f"Generaciones completadas: {self.ga.generation}").pack(anchor='w')
        ttk.Label(info_frame, text=f"Tamaño población: {self.ga.population_size}").pack(anchor='w')

    def _crear_pestana_caracteristicas(self, parent):
        """Crea el contenido de la pestaña de características"""
        if not hasattr(self, 'features'):
            ttk.Label(parent, text="No hay datos de características disponibles").pack()
            return
        
        # Frame desplazable
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mostrar características en dos columnas
        for i, (key, value) in enumerate(self.features.items()):
            row = i // 2
            col = i % 2
            
            frame = ttk.Frame(scrollable_frame)
            frame.grid(row=row, column=col, sticky='ew', padx=5, pady=2)
            
            ttk.Label(frame, text=f"{key.replace('_', ' ').title()}: ", 
                     font=('Arial', 9, 'bold')).pack(side='left')
            ttk.Label(frame, text=f"{value if not isinstance(value, float) else f'{value:.4f}'}").pack(side='left')
        

    def exportar_datos(self):
        """Exporta ambos archivos CSV (generaciones y características)"""
        if not hasattr(self, 'ga') or not hasattr(self, 'features'):
            messagebox.showwarning("Advertencia", "No hay datos para exportar")
            return
        
        # Pedir directorio donde guardar
        dir_path = filedialog.askdirectory(title="Seleccionar carpeta para guardar los archivos")
        if not dir_path:
            return
        
        try:
            # 1. CSV del historial de generaciones
            generaciones_path = f"{dir_path}/generaciones_{self.features['Instancia'].replace('.csv', '')}"
            self._exportar_generaciones(generaciones_path)
            
            # 2. CSV de características
            caracteristicas_path = f"{dir_path}/caracteristicas_{self.features['Instancia'].replace('.csv', '')}"
            self._exportar_caracteristicas(caracteristicas_path)
            
            messagebox.showinfo(
                "Éxito", 
                f"Archivos exportados correctamente:\n\n"
                f"1. {generaciones_path}.csv\n"
                f"2. {caracteristicas_path}.csv"
            )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron exportar los archivos:\n{str(e)}")

    def _exportar_generaciones(self, base_path):
        """Exporta el historial de generaciones a CSV"""
        data = {
            'Generación': list(range(len(self.historial_fitness))),
            'Mejor Fitness': self.historial_fitness
        }
        
        # Agregar estadísticas adicionales si están disponibles
        if hasattr(self.ga, 'generation_stats'):
            stats = self.ga.generation_stats
            data['Fitness Promedio'] = [gen_stats.get('avg', '') for gen_stats in stats]
            data['Peor Fitness'] = [gen_stats.get('min', '') for gen_stats in stats]
        
        df = pd.DataFrame(data)
        df.to_csv(f"{base_path}.csv", index=False)

    def _exportar_caracteristicas(self, base_path):
        """Exporta las características de la instancia a CSV"""
        df = pd.DataFrame([self.features])
        
        # Reordenar columnas para mejor presentación
        cols = ['Instancia', 'n', 'm', 'n_m'] + [c for c in df.columns if c not in ['Instancia', 'n', 'm', 'n_m']]
        df = df[cols]
        
        df.to_csv(f"{base_path}.csv", index=False)